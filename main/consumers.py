import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import subprocess

class CodeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        code = data['code']
        question_id = data['question_id']

        # Execute the code
        output = await sync_to_async(self.execute_code)(code)

        # Check the output against test cases
        correct = await sync_to_async(self.check_output)(question_id, output)

        await self.send(text_data=json.dumps({
            'output': output,
            'correct': correct,
        }))

    def execute_code(self, code):
        # You may want to run the code inside a Docker container for security
        process = subprocess.Popen(
            ['python3', '-c', code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        return stdout.decode() if stdout else stderr.decode()

    def check_output(self, question_id, output):
        # Fetch the correct output from the database and compare
        correct_output = 'expected output'  # Placeholder
        return output.strip() == correct_output.strip()
