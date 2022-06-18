import tekore as tk

def pedir_token() -> None:
    client_id = '6d3faa7cfb01460bacc1605a2f508e0d'
    client_secret = '1e159178e8ca443498e3ec58f25fd792'
    redirect_uri = 'https://example.com/callback'
    conf = (client_id, client_secret, redirect_uri)
    file = 'tekore.cfg'

    token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)
    tk.config_to_file(file, conf + (token.refresh_token,))