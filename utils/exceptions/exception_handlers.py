from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None and isinstance(response.data, dict):
        if not response.data.get('detail'):
            details = []

            for field_name in response.data.keys():
                if field_name == 'non_field_errors':
                    details += response.data.get(field_name, [])
                else:
                    message = ','.join(response.data.get(field_name, [])).lower()
                    details.append(f'{field_name.capitalize()} - {message}')

            response.data['detail'] = ' '.join(details)

        response.data['status'] = 'ok' if response.status_code in [200, 201] else 'error'
    return response
