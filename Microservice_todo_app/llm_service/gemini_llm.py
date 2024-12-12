print("ผู้ช่วยอัจฉริยะ ช่วยแนะนำตารางชีวิตให้ตาม user_id ให้คำปรึกษาผ่านช่องแชทโดยมีข้อมูล task และ room ของ user เป็น base prompt เสมอ")
#สมมุติว่ามันเป็นแชทบอทบนหน้า frontend ที่มันจะมี data ของเราทั้งหมดใน todo list

import google.generativeai as genai
import os
import requests
import json
from flask import Flask, request, jsonify

from dotenv import load_dotenv
load_dotenv()
google_api_key = os.getenv("GEMINI")

app = Flask(__name__)

@app.route('/llm', methods=['GET'])
def get_llm_response():

    json_body = request.get_json()
    #ดึง value ออกมาจาก key json
    user_id = json_body.get('user_id')
    # print('here is user_id', data['user_id'])
    url = {
    # "user":"http://localhost:5001",
    "task":"http://localhost:5002"
    }

    r = requests.get(f"{url['task']}/llm/query/tasks/{user_id}")
    data = json.loads(r.text)

    print(data)

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    system_prompt = f"""
    สวมบทบาทเป็นนักวางแผนการทำงานเชี่ยวชาญเรื่องการบริหารเวลา
    นี่คืองานของผมใน todo list โดยใน todo list จะมีห้องแยกเพื่อแบ่งส่วนงานชัดเจนเป็นโปรเจค หรือรายวิชาย่อย
    {data}
    คุณต้องใช้ข้อมูลนี้เพื่อแนะนำผมในสิ่งที่ผมจะถามถัดจากนี้->
    """

    # user_prompt = "คุณช่วยวางแผนให้ผมหน่อยผมควรจะทำงานไหนก่อน สมมุติผมมี data เพิ่มคือ todo 'ช่วยการบ้านบวกเลขป.1 ให้ น้องด้วย' "
    user_prompt = json_body.get('prompt')

    end_prompt = "สุดท้ายนี้ถ้ามีการ ถามตอบกันไปมาเรื่อยๆ คุณจะโฟกัสเพียงแค่ข้อความหลังจาก '\\n->' เท่านั้นเพราะที่เหลือมันคือ system prompt ไม่จำเป็นต้องอ่านซ้ำ"
    

    full_prompt = f"""{system_prompt}\n{user_prompt} {end_prompt}"""

    response = model.generate_content(full_prompt)
    print(response.text)

    return jsonify({"llm_message": response.text}), 200
        

if __name__ == '__main__':
    app.run(port=5004,debug=True)


#ลองเทส api ตั้งแต่อันแรกสุดด้วย


