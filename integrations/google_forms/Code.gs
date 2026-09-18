// Run setupEmployeeForm() once from a Google Apps Script project owned by the company.
// Never collect TikTok passwords or access tokens in this form.
const FIELDS = ['社員ID', '氏名', 'TikTokアカウント名', '発信ジャンル', '1日の希望投稿本数'];
const ADMIN_COLUMNS = ['登録状態', '管理者確認日時', '管理者メモ'];

function setupEmployeeForm() {
  const props = PropertiesService.getScriptProperties();
  if (props.getProperty('FORM_ID')) throw new Error('Already initialized; do not create duplicate forms');
  const sheet = SpreadsheetApp.create('TikTok AI 社員登録台帳');
  const form = FormApp.create('TikTok AI 社員登録フォーム');
  form.setDescription('社員登録用。TikTokのパスワード・認証コードは絶対に入力しないでください。登録後、管理者の承認を経て運用を開始します。');
  form.addTextItem().setTitle(FIELDS[0]).setRequired(true);
  form.addTextItem().setTitle(FIELDS[1]).setRequired(true);
  form.addTextItem().setTitle(FIELDS[2]).setRequired(true);
  form.addParagraphTextItem().setTitle(FIELDS[3]).setRequired(true);
  form.addListItem().setTitle(FIELDS[4]).setChoiceValues(['1', '2']).setRequired(true);
  form.setDestination(FormApp.DestinationType.SPREADSHEET, sheet.getId());
  props.setProperties({FORM_ID: form.getId(), SHEET_ID: sheet.getId()});
  ScriptApp.newTrigger('onEmployeeSubmit').forSpreadsheet(sheet).onFormSubmit().create();
  Logger.log('フォーム（社員に共有）: ' + form.getPublishedUrl());
  Logger.log('台帳（管理者のみ）: ' + sheet.getUrl());
}

function onEmployeeSubmit(event) {
  if (!event || !event.range) throw new Error('Spreadsheet form-submit trigger required');
  const sheet = event.range.getSheet();
  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  let statusCol = headers.indexOf(ADMIN_COLUMNS[0]) + 1;
  if (!statusCol) {
    statusCol = headers.length + 1;
    sheet.getRange(1, statusCol, 1, ADMIN_COLUMNS.length).setValues([ADMIN_COLUMNS]);
  }
  sheet.getRange(event.range.getRow(), statusCol).setValue('承認待ち');
}

// Administrator-controlled export. Run only after manually setting 登録状態 to 承認済み.
// Exports a JSON file to the company's Drive; it does NOT publish a public URL or
// automatically transmit employee personal information to GitHub.
function exportApprovedRoster() {
  const id = PropertiesService.getScriptProperties().getProperty('SHEET_ID');
  if (!id) throw new Error('Run setupEmployeeForm first');
  const spreadsheet = SpreadsheetApp.openById(id);
  const sheet = spreadsheet.getSheets().find(s => s.getName().includes('フォームの回答') || s.getName().includes('Form Responses'));
  if (!sheet) throw new Error('Form response sheet not found');
  const rows = sheet.getDataRange().getValues();
  const columns = rows.shift().map(String);
  const required = [...FIELDS, ADMIN_COLUMNS[0]];
  if (required.some(field => !columns.includes(field))) throw new Error('Missing required columns');
  const seen = new Set();
  const accounts = [];
  for (const row of rows) {
    const get = key => String(row[columns.indexOf(key)] ?? '').trim();
    if (get(ADMIN_COLUMNS[0]) !== '承認済み') continue;
    const employeeId = get('社員ID');
    if (!/^[a-zA-Z0-9_-]{2,40}$/.test(employeeId) || seen.has(employeeId)) throw new Error('Invalid or duplicate employee ID: ' + employeeId);
    seen.add(employeeId);
    const posts = Number(get('1日の希望投稿本数'));
    if (![1, 2].includes(posts)) throw new Error('Invalid post count for ' + employeeId);
    if (!get('氏名') || !get('TikTokアカウント名') || !get('発信ジャンル')) throw new Error('Incomplete approved employee: ' + employeeId);
    accounts.push({employee_id: employeeId, name: get('氏名'), account: get('TikTokアカウント名'), niche: get('発信ジャンル'), posts_per_day: posts, status: 'active'});
  }
  const payload = JSON.stringify({schema_version: 1, exported_at: new Date().toISOString(), accounts}, null, 2);
  const file = DriveApp.createFile('tiktok-approved-roster.json', payload, MimeType.PLAIN_TEXT);
  Logger.log('承認済み社員台帳: ' + file.getUrl() + ' / ' + accounts.length + '名');
}
