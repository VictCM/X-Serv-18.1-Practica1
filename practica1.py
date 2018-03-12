#!/usr/bin/python3

import webapp
import csv

class datosApp (webapp.webApp):

    # Diccionarios
    Real = {}
    Acortada = {}

    def leer(self):
        try:
            with open("urls.csv") as csfile:
                datos = csv.reader(csfile)
                for fila in datos:
                    num = int(fila[0])
                    url= fila[1]
                    self.Real[num] = url
                    self.Acortada[url] = num
        except FileNotFoundError:
            print("No se encuentra archivo")

    def escribir(self):
        with open("urls.csv", "w") as csvfile:
            escr = csv.writer(csvfile)
            for url in self.Real:
                escr.writerow([url, self.Real[url]])

    def parse(self, request):
        self.leer()  # Lee el fichero
        return (request.split(' ', 1)[0],
                request.split(' ', 2)[1],
                request.split('\r\n\r\n')[-1])

    def process(self, parsed):
        metodo, peticion, body = parsed
        if (peticion == "/"):
            if (metodo == "GET"):
                httpCode = "200 OK"
                htmlBody = ("<html><body><form method= 'POST' action=''>" +
                            "<input type = 'text' name= 'url'>" +
                            "<input type= 'submit' value='Enviar'></form>" +
                            "<p>" + str(self.Real) + "</p></html>")
            elif (metodo == "POST"):
                import urllib.parse
                url = urllib.parse.unquote(body)
                if ("=" in body):      # Comparo lo que envio, si hay QS entra
                    url = url.split('=')[-1]
                    if not url.startswith("https://") and not url.startswith("http://"):
                        url = "http://" + url

                    if (url in self.Acortada): #Comparo si ya la tengo
                        httpCode = "404 Not Found"
                        htmlBody = ("<html><body>Ya esta guardado con URL: <a href = " +
                                    'http://localhost:1234/' + str(self.Acortada[url]) +
                                    ">"+ 'http://localhost:1234/' + str(self.Acortada[url]) + "</a></body></html>")
                    else:
                        self.Real[len(self.Real)] = url
                        self.Acortada[url] = len(self.Acortada)
                        self.escribir()
                        httpCode = "200 OK"
                        htmlBody = ("<html><body><p><a href = " +
                                    self.Real[(len(self.Real) - 1)] +
                                    ">" +
                                    self.Real[(len(self.Real) - 1)] +
                                    "</a></p><p><a href = " +
                                    self.Real[(len(self.Real) - 1)] +
                                    ">" + 'http://localhost:1234/' +
                                    str(len(self.Real) - 1) +
                                    "</a></p></body></html>")
                else:
                    httpCode = "400 Bad Request" #Error mio al enviar
                    htmlBody = ("<html><body>Error en el request</html>")
            else:
                httpCode = "405 Method Not Allowed"
                htmlBody = ("<html><body>No se puede utilizar ese metodo</html>")

        else:
            peticion = peticion.split("/")[-1]
            if (peticion == "favicon.ico"): #Si me encuentro un favicon.ico
                httpCode = "404 Not Found"
                htmlBody = ("<html><body>Favicon</html>")
                recvSocket.close()
            elif (int(peticion) in self.Real):
                peticion = int(peticion)
                httpCode = "301 Moved Permanently"
                htmlBody = ("<html><meta http-equiv= 'Refresh'" +
                            "content =3; url=" + self.Real[peticion] +
                            ">\r\n" +
                            "<html><body><p> Seras redirigido a: " +
                            self.Real[peticion] +
                            "</p></body></html>")
            else:
                httpCode = "404 Not Found"
                htmlBody = ("<html><body>No encontrado</html>")

        return (httpCode, htmlBody)

if __name__ == "__main__":
    testWebApp = datosApp("localhost", 1234)
