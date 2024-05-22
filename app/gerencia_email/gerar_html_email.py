def corpo_email(
    nome_cliente, TextoIntrodutivo, TextContainer2, TextContainer3, btn_ver_mais
):
    link = "https://comercioprime.azurewebsites.net/"

    # Montar o corpo do email em HTML com base nas variáveis
    html_body = f"""
    <head>
        <style>
            .highlighted {{
                color: #DF6316;
                font-family: "Arial", sans-serif;
                font-size: 30px;
            }}
        </style>
    </head>
    <body>

    <!--header padrão -->
    <div style="text-align: center;">
        <img alt="Logo da Empresa" style="width: 100%;" src="https://comercioprime.azurewebsites.net/assents/img/biblioteca/name-empresa.png">
        <br>
    </div>

    <!--main padrão -->
    <div style="center;background: #white;border: none;border-radius: 20px;padding: 10px 30px;">
        <p style="font-size: 20px; font-family: Arial, sans-serif; color: #333;">
            {'Prezado ' + nome_cliente + ',' if nome_cliente else ''}
            <br><br>
            {TextoIntrodutivo}
        </p>
    </div>

    <!--texto secundário caso a var TextContainer2 for diferente de null, colocamos o container como visível -->
    {'<div style="text-align: center;background: #DF6316;border: none; border-radius: 20px; padding: 10px 30px;">'
     '<p style="font-size: 20px; font-family: Arial, sans-serif; color: #333;">'
     f'{TextContainer2}'   
     '<br><br>'
     '</p>'
     '</div>' if TextContainer2 else ''}

    <!--texto secundário caso a var TextContainer3 for diferente de null, colocamos o container como visível -->
    {'<div style="text-align: center;background: #0d1b2a;border: none;border-radius: 20px;padding: 10px 30px;margin: 15px 0 15px 0;">'
     '<p style="font-size: 20px;font-family: Arial, sans-serif;color: #fff;">'
     f'{TextContainer3}'  
     '</p>'
     '</div>' if TextContainer3 else ''}

    <!--precisamos de um if caso o valor bool for True, coloco o botão como visível -->
    {'<div style="text-align: center;">'
     '<a href="{link}" style="text-decoration: none;">'
     '<button style="background-color: #00bf63; color: dark; border: none; border-radius: 20px; padding: 10px 30px; font-weight: bold; cursor: pointer;">'
     'Saiba mais'
     '</button>'
     '</a>'
     '</div>' if btn_ver_mais else ''}

    <!--rodapé padrão -->
    
    <div style="text-align:center;background: #000000;border: none; ;font-size: 10px;color: white;margin:10px 0 0 0">
      
        <img alt="Logo da Empresa" style="width: 100%" src="https://comercioprime.azurewebsites.net/assents/img/biblioteca/banner-frase.png">
        <br>
        Atenciosamente, Samuel Medeiros
        <br>
    <div style="padding: 10px 30px">
            <a href="{link}" style="font-size:8px;color: #DF6316;text-align:center">Caso tenha alguma dúvida ou precise de assistência, nossa equipe de suporte estará à disposição para ajudar.</a>
    </div>  </div>
    </div>
 
    </body>
    """

    return html_body
