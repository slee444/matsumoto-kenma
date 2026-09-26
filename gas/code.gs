/**
 * 松本研磨工業 お問い合わせフォーム受信スクリプト（Google Apps Script）
 *
 * できること
 *  - 研磨／Web集客 どちらのフォームからの送信も受け付ける
 *  - 管理者（ADMIN_EMAIL）に通知メールを送る（どのページから来たかも記載）
 *  - お客様に、受付メール（控え）を自動で送る（悪用防止のため回数制限あり・入力内容は載せない）
 *  - SHEET_ID を設定すると、スプレッドシートにも1行ずつ記録する
 *
 * 設置・更新のしかた（今のフォームのURLを変えずに更新する方法）
 *  1. https://script.google.com を開き、今フォームで使っているプロジェクトを開く
 *  2. 「コード.gs」の中身をすべて、このファイルの内容に置きかえて保存
 *  3. 右上「デプロイ」→「デプロイを管理」→ 鉛筆マーク（編集）
 *     → バージョン：「新バージョン」を選んで「デプロイ」
 *     ※「新しいデプロイ」を作るとURLが変わるので、必ず「デプロイを管理」から更新する
 *  4. 初回はメール送信の許可を求められるので「許可」する
 *  5. サイトのフォームからテスト送信し、管理者とお客様の両方にメールが届くか確認
 *
 * 送信元について
 *  メールは、このスクリプトを所有するGoogleアカウントから送られます。
 *  お客様への控えメールは「返信先」を ADMIN_EMAIL にしているので、
 *  お客様が返信すると ADMIN_EMAIL に届きます。
 */

var ADMIN_EMAIL = 'm.m@matsumoto-kenma.co.jp';
var COMPANY = '株式会社松本研磨工業';
var TEL = '044-333-8412';
var SHEET_ID = ''; // 記録したいスプレッドシートのID（空なら記録しない）

// 悪用対策（第三者へのメール大量送信を防ぐ）
var REPLY_INTERVAL_SEC = 600;  // 同じアドレスへの控えメールは10分に1通まで
var REPLY_PER_HOUR = 20;       // 控えメールは全体で1時間20通まで
var QUOTA_RESERVE = 20;        // 1日の送信上限が残りこれ以下なら控えを送らず、管理者通知を優先
var MAX_FIELD_LEN = 3000;      // 1項目あたりの最大文字数

var FORM_NAMES = {
  polishing: '金属研磨',
  web: 'Web集客・AI活用支援'
};

function doPost(e) {
  try {
    var p = parsePayload_(e);
    if (p.hp) return json_({ ok: true }); // スパム対策（人には見えない欄に入力があれば捨てる）

    var formName = FORM_NAMES[p.formType] || 'お問い合わせ';
    var name = oneLine_(p.name).slice(0, 50) || '（お名前未記入）';
    var email = oneLine_(p.email);
    var now = Utilities.formatDate(new Date(), 'Asia/Tokyo', 'yyyy/MM/dd HH:mm');

    var body = (p.fields || [])
      .filter(function (f) { return f[1]; })
      .map(function (f) { return '■' + f[0] + '\n' + String(f[1]).slice(0, MAX_FIELD_LEN); })
      .join('\n\n');

    var meta =
      '■問い合わせ前に見ていたページ\n' + (p.sourceUrl || '（不明）') + '\n\n' +
      '■フォームのページ\n' + (p.pageUrl || '（不明）') + '\n\n' +
      '■受付日時\n' + now;

    // 1) 管理者への通知
    MailApp.sendEmail({
      to: ADMIN_EMAIL,
      replyTo: isEmail_(email) ? email : ADMIN_EMAIL,
      subject: '【' + formName + '】お問い合わせ：' + name + ' 様',
      name: COMPANY + ' ホームページ',
      body: formName + 'のフォームからお問い合わせがありました。\n\n' + body + '\n\n' +
            '──────────────\n' + meta
    });

    // 2) お客様への控え
    //    Web集客・AI活用支援は、会社の電話ではなく専用フォームで受け付けるため電話番号を載せない
    //    悪用防止のため、送信回数を制限し、入力内容（自由記述）はメールに載せない
    if (isEmail_(email) && canSendReply_(email)) {
      var isWeb = p.formType === 'web';
      var sender = isWeb ? 'マツケンスタジオ（' + COMPANY + '）' : COMPANY;
      var footer = isWeb
        ? 'マツケンスタジオ by ' + COMPANY + '\n' + 'https://matsumoto-kenma.co.jp/web-ai/'
        : COMPANY + '\n' + '〒210-0851 神奈川県川崎市川崎区浜町3-9-22\n' + 'TEL ' + TEL + '\n' + 'https://matsumoto-kenma.co.jp/';
      var urgent = isWeb ? '' : '※お急ぎの場合は、お電話（' + TEL + '／平日8:30〜18:00）でもご連絡いただけます。\n';
      MailApp.sendEmail({
        to: email,
        replyTo: ADMIN_EMAIL,
        subject: '【' + sender + '】お問い合わせを受け付けました',
        name: sender,
        body: name + ' 様\n\n' +
              'このたびはお問い合わせいただき、ありがとうございます。\n' +
              '【' + formName + '】のお問い合わせを受け付けました。\n' +
              '内容を確認のうえ、担当者よりご連絡いたします。\n\n' +
              '※このメールは自動でお送りしています。\n' + urgent +
              '※このメールに返信いただくと、担当者に届きます。\n\n' + footer
      });
    }

    // 3) スプレッドシートに記録（任意）
    if (SHEET_ID) {
      var sheet = SpreadsheetApp.openById(SHEET_ID).getSheets()[0];
      sheet.appendRow([now, formName, name, email, body, p.sourceUrl || '', p.pageUrl || '']);
    }

    return json_({ ok: true });
  } catch (err) {
    // エラー通知も連続では送らない（10分に1通まで）
    var cache = CacheService.getScriptCache();
    if (!cache.get('err_notified')) {
      cache.put('err_notified', '1', 600);
      MailApp.sendEmail(ADMIN_EMAIL, '【要確認】フォームの送信処理でエラー',
        String(err) + '\n\n' + JSON.stringify(e && e.parameter).slice(0, 5000));
    }
    return json_({ ok: false });
  }
}

// 新しい形式（payload）と、以前の形式（項目がそのまま届く）の両方に対応
function parsePayload_(e) {
  var prm = (e && e.parameter) || {};
  if (prm.payload) return JSON.parse(prm.payload);
  var labels = { name: 'お名前', company: '会社名・屋号', email: 'メールアドレス', tel: '電話番号',
    type: 'お問い合わせの種別', process: 'ご希望の加工', material: '材質', quantity: '数量（概算）',
    deadline: 'ご希望納期', message: 'お問い合わせ内容' };
  var fields = Object.keys(labels).map(function (k) { return [labels[k], prm[k] || '']; });
  return { formType: 'polishing', name: prm.name, email: prm.email, fields: fields };
}

// 控えメールを送ってよいか（同じアドレスへの連続送信・全体の送信数・1日の上限を確認）
function canSendReply_(email) {
  if (MailApp.getRemainingDailyQuota() <= QUOTA_RESERVE) return false;
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(5000)) return false;
  try {
    var cache = CacheService.getScriptCache();
    var addrKey = 'r_' + Utilities.base64EncodeWebSafe(email.toLowerCase()).slice(0, 200);
    if (cache.get(addrKey)) return false;
    var hourKey = 'h_' + Utilities.formatDate(new Date(), 'Asia/Tokyo', 'yyyyMMddHH');
    var count = Number(cache.get(hourKey) || 0);
    if (count >= REPLY_PER_HOUR) return false;
    cache.put(hourKey, String(count + 1), 3600);
    cache.put(addrKey, '1', REPLY_INTERVAL_SEC);
    return true;
  } finally {
    lock.releaseLock();
  }
}

function oneLine_(s) { return String(s || '').replace(/[\r\n]+/g, ' ').trim(); }
function isEmail_(s) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s || ''); }
function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
