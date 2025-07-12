import os
import openai
from typing import List, Dict

class AIService:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
    def search_documents(self, query: str, documents: List[Dict]) -> str:
        """Поиск по документам с помощью OpenAI"""
        try:
            # Формируем контекст из документов
            context = self._prepare_context(documents)
            
            # Создаем промпт для поиска
            prompt = f"""
            Контекст из документов:
            {context}
            
            Вопрос пользователя: {query}
            
            Ответь на вопрос пользователя, используя информацию из предоставленных документов. 
            Если в документах нет информации для ответа, скажи об этом.
            Отвечай кратко и по существу.
            """
            
            # Отправляем запрос к OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты помощник по работе с корпоративными документами. Отвечай кратко и по существу."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Ошибка при обработке запроса: {str(e)}"
    
    def _prepare_context(self, documents: List[Dict]) -> str:
        """Подготовка контекста из документов"""
        context_parts = []
        
        for doc in documents:
            name = doc.get('name', 'Неизвестный документ')
            content = doc.get('content', '')
            
            # Ограничиваем размер контента
            if len(content) > 1000:
                content = content[:1000] + "..."
            
            context_parts.append(f"Документ: {name}\nСодержание: {content}\n")
        
        return "\n".join(context_parts)
    
    def get_document_summary(self, document_name: str, content: str) -> str:
        """Получение краткого описания документа"""
        try:
            prompt = f"""
            Документ: {document_name}
            Содержание: {content[:1000]}...
            
            Сделай краткое описание этого документа (2-3 предложения).
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты помощник по анализу документов."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.5
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Ошибка при создании описания: {str(e)}" 