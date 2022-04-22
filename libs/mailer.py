import os, json, requests
from dotenv import load_dotenv


load_dotenv()
MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')

class Mailer():

    @classmethod
    def send_mail(cls, send_to: str, variables: dict) -> None:
        print('\n 💌 SENDING MAIL...')
        data = cls._get_base_data(send_to)
        cls._add_variables(data, variables)

        requests.post(
            url=f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data=data
        )
        print(' ✅ DONE!')

    @staticmethod
    def _get_base_data(send_to: str) -> dict:
        return {
            'to': send_to,
            'template': 'superhero_template',
            'from': 'LIDS Newsletter <cnsfeir@uc.cl>',
            'subject': '[Liga Interdimensional de Superhéroes] Última Fecha',
        }

    @staticmethod
    def _add_variables(data: dict, variables: dict) -> None:
        header_variables = {}
        for key, value in variables.items():
            if 'iterable.' in key:
                header_variables.update({key.replace('iterable.', ''): value})
            else:
                data[f'v:{key}'] = value

        data['h:X-Mailgun-Variables'] = json.dumps(header_variables)
