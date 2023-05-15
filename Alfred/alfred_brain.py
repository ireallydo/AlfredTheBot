from settings import OPENAI_TOKEN
import openai


openai.api_key = OPENAI_TOKEN


class AlfredBrain:

    @staticmethod
    async def think_about_it(prompt):
        response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                temperature=0.2,
                max_tokens=100,
                top_p=1,
                n=1,
                frequency_penalty=0.2,
                presence_penalty=0,
                stop=[" \n"]
        )
        resp = response["choices"][0]["text"]
        # TODO delete - debugging printout
        print("The summarized text is:")
        print(resp)
        # return f"That's what I think about it, sir: {resp}"
        return resp


alfred_brain = AlfredBrain()
