import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

class GoogleDriveService:
    def __init__(self):
        self.creds = None
        self.service = None
        self.folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        
    def authenticate(self):
        """Аутентификация в Google Drive API"""
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
        
        self.service = build('drive', 'v3', credentials=self.creds)
    
    def get_documents(self):
        """Получение списка документов из папки"""
        if not self.service:
            self.authenticate()
        
        results = self.service.files().list(
            q=f"'{self.folder_id}' in parents and (mimeType contains 'document' or mimeType contains 'spreadsheet' or mimeType contains 'pdf')",
            pageSize=100,
            fields="files(id, name, mimeType, webViewLink)"
        ).execute()
        
        return results.get('files', [])
    
    def get_document_content(self, file_id, mime_type):
        """Получение содержимого документа"""
        if not self.service:
            self.authenticate()
        
        try:
            if 'document' in mime_type:
                return self._get_google_doc_content(file_id)
            elif 'spreadsheet' in mime_type:
                return self._get_google_sheet_content(file_id)
            elif 'pdf' in mime_type:
                return self._get_pdf_content(file_id)
            else:
                return f"Неподдерживаемый тип файла: {mime_type}"
        except Exception as e:
            return f"Ошибка при получении содержимого: {str(e)}"
    
    def _get_google_doc_content(self, file_id):
        """Получение содержимого Google Doc"""
        try:
            from googleapiclient.discovery import build
            docs_service = build('docs', 'v1', credentials=self.creds)
            document = docs_service.documents().get(documentId=file_id).execute()
            
            content = []
            for element in document.get('body', {}).get('content', []):
                if 'paragraph' in element:
                    for para_element in element['paragraph']['elements']:
                        if 'textRun' in para_element:
                            content.append(para_element['textRun']['content'])
            
            return ''.join(content)
        except Exception as e:
            return f"Ошибка при чтении Google Doc: {str(e)}"
    
    def _get_google_sheet_content(self, file_id):
        """Получение содержимого Google Sheet"""
        try:
            sheets_service = build('sheets', 'v4', credentials=self.creds)
            sheet = sheets_service.spreadsheets().get(spreadsheetId=file_id).execute()
            
            content = []
            for worksheet in sheet.get('sheets', []):
                title = worksheet['properties']['title']
                content.append(f"Лист: {title}")
                
                range_name = f"{title}!A1:Z1000"
                result = sheets_service.spreadsheets().values().get(
                    spreadsheetId=file_id, range=range_name).execute()
                
                values = result.get('values', [])
                for row in values:
                    content.append(' | '.join(str(cell) for cell in row))
                content.append('\n')
            
            return '\n'.join(content)
        except Exception as e:
            return f"Ошибка при чтении Google Sheet: {str(e)}"
    
    def _get_pdf_content(self, file_id):
        """Получение содержимого PDF (базовая реализация)"""
        try:
            request = self.service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            
            # Простое извлечение текста (в реальном проекте нужен pdfplumber или pytesseract)
            return f"PDF файл загружен (размер: {len(file.getvalue())} байт). Для полного извлечения текста нужны дополнительные библиотеки."
        except Exception as e:
            return f"Ошибка при чтении PDF: {str(e)}" 