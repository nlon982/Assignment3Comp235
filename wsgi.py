from CS235Flix import create_app

app = create_app()

if __name__ == "__main__":
        app.run(host = "localhost", port = 5000, threaded = False) # localhost is a special value which gives you 127.0.0.1, always?
