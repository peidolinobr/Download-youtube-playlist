import traceback
try:

    import os
    from pytube import YouTube
    from pytube import Playlist
    from moviepy.editor import *
    import easygui
    import re

    def baixar_playlist_mp3(url_playlist, pasta_destino='.'):
        tipoArquivo = easygui.ynbox('Deseja em qual formato?', 'Escolha uma opção', choices=["Mp3", "Mp4"])
        if tipoArquivo == None:
            tipoArquivo = True
            
        # Identifica se é playlist ou musica única
        playlist = Playlist(url_playlist)
        try:
            print(playlist)
        except:
            playlist = [url_playlist]
        
        quantidade_musicas = len(playlist)
        quantidade_digitos = len(str(len(playlist)))

        # Itera sobre os vídeos da playlist
        contador = 1
        for video_url in playlist:
    
            # Cria uma instância do objeto YouTube
            yt = YouTube(video_url)
            
            # Define uma expressão regular para manter apenas caracteres alfanuméricos, espaços e pontos
            padrao = re.compile(r'[^a-zA-Z0-9\s.]')
            
            # Substitui caracteres não permitidos por sublinhados
            nome_limpo = re.sub(padrao, '_', yt.title)

            # Obtém a stream de áudio
            audio_stream = yt.streams.filter(only_audio=True).first()
            
            #faz download
            nome_arquivo = f"{str(contador).zfill(quantidade_digitos)} {nome_limpo}.mp4"
            audio_stream.download(output_path=pasta_destino, filename=nome_arquivo)
            print(f'{round(contador*100/quantidade_musicas, 2)}%')
            
            if tipoArquivo == True:
                #converte arquivo para mp3
                caminho_completo_mp4 = os.path.join(pasta_destino, nome_arquivo)
                nome_arquivo_novo = f"{str(contador).zfill(quantidade_digitos)} {nome_limpo}.mp3"
                arquivo = AudioFileClip(caminho_completo_mp4)
                arquivo.write_audiofile(os.path.join(pasta_destino, nome_arquivo_novo))
                arquivo.close()
                
                #remove arquivo mp4
                os.remove(caminho_completo_mp4)
            
            contador += 1
        os.startfile(pasta_destino)
        easygui.msgbox('Todas os vídeos/músicas foram baixados', 'Finalizando')

    # Exemplo de uso
    url_da_playlist = None
    resposta = True
    while (url_da_playlist == None and resposta != False):
        url_da_playlist = easygui.enterbox('Qual o link da musica/playlist?', 'Link solicitado')
        if url_da_playlist == None:
            resposta = easygui.ynbox('Preciso do link, gostaria de tentar novamente?', 'Escolha uma opção', choices=["Sim", "Não"])

    if url_da_playlist != None:

        pasta_destino = None
        resposta = True

        while (pasta_destino == None and resposta != False):
            pasta_destino = easygui.diropenbox(title="Selecione uma Pasta")
            if pasta_destino == None:
                resposta = easygui.ynbox('Preciso da pasta, gostaria de tentar novamente?', 'Escolha uma opção', choices=["Sim", "Não"])
        
    baixar_playlist_mp3(url_da_playlist, pasta_destino)

    
except Exception as e:
    traceback.print_exc()
    input()