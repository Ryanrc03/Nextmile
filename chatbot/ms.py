from openai import OpenAI
from db_config import db_handler
import time
import uuid
from admin_api import router as admin_router

client = OpenAI(
    base_url='https://api-inference.modelscope.cn/v1',
    api_key='ms-74b8eedd-5f76-419a-a513-f421399093da', # ModelScope Token
)

app.include_router(admin_router)

# 假设您有一个处理查询的端点
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    start_time = time.time()
    session_id = request.session_id or str(uuid.uuid4())
    
    try:
        response = client.chat.completions.create(
            model='deepseek-ai/DeepSeek-V3.1', # ModelScope Model-Id, required
            messages=[
                {
                    'role': 'user',
                    'content': request.query
                }
            ],
            stream=True
        )
        done_reasoning = False
        for chunk in response:
            reasoning_chunk = chunk.choices[0].delta.reasoning_content
            answer_chunk = chunk.choices[0].delta.content
            if reasoning_chunk != '':
                print(reasoning_chunk, end='',flush=True)
            elif answer_chunk != '':
                if not done_reasoning:
                    print('\n\n === Final Answer ===\n')
                    done_reasoning = True
                print(answer_chunk, end='',flush=True)
        
        # 计算响应时间
        response_time = time.time() - start_time
        
        # 保存到MongoDB
        conversation_id = await db_handler.save_conversation_async(
            user_query=request.query,
            bot_response=answer_chunk,
            session_id=session_id,
            user_id=request.user_id,
            response_time=response_time,
            model_used="your_model_name"
        )
        
        return {
            "response": answer_chunk,
            "session_id": session_id,
            "conversation_id": conversation_id,
            "response_time": response_time
        }
        
    except Exception as e:
        # 错误情况也可以记录
        await db_handler.save_conversation_async(
            user_query=request.query,
            bot_response=f"Error: {str(e)}",
            session_id=session_id,
            user_id=request.user_id,
            response_time=time.time() - start_time,
            model_used="error"
        )
        raise e