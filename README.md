# Utilizadores ligados

Aplicação GNOME em Flatpak que lista utilizadores com uma sessão de utilizador
no systemd-logind. Atualize a lista pelo botão na janela.

## Instalar e executar

O pacote `.flatpak` não é guardado no Git. Se ainda não o tiver, crie-o
seguindo as instruções abaixo.

Instale para o utilizador atual:

```sh
flatpak install --user ./com.jfscorreia.usersList.flatpak
flatpak run com.jfscorreia.usersList
```

Para instalar para todos os utilizadores, use `--system` em vez de `--user`:

```sh
flatpak install --system ./com.jfscorreia.usersList.flatpak
```

O Flatpak precisa estar instalado e o systemd-logind acessível no anfitrião.
Sessões de greeter e de gestor não aparecem na lista.

O pacote indica o Flathub como fonte do runtime GNOME 50. Se este ainda não estiver
instalado, o Flatpak pode pedir confirmação para o configurar e descarregar.
Para descarregá-lo é necessária ligação à internet; se não puder ser obtido, a
instalação apresenta um erro. O pacote não inclui o runtime nem fornece
atualizações automáticas da aplicação.

O novo identificador é distinto do antigo `io.github.jops3.GnomeWViewer`.
Se instalou anteriormente essa versão, pode removê-la com
`flatpak uninstall --user io.github.jops3.GnomeWViewer`.

A aplicação requer o systemd-logind no anfitrião e tem permissão para comunicar
com `org.freedesktop.login1` no D-Bus do sistema.

## Criar o Flatpak

Para criar o pacote, instale Python 3, Flatpak e o runtime GNOME 50 para a
arquitetura da máquina de compilação. Por exemplo:

```sh
flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install --user flathub org.gnome.Platform//50
python3 build-flatpak.py
```

O ficheiro `com.jfscorreia.usersList.flatpak` é criado nesta pasta e serve
para máquinas com a mesma arquitetura.
