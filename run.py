from app import create_app

application = create_app()

if __name__ == '__main__':

    application.run(
        host=application.config.get('HOST'),
        port=application.config.get('PORT'),
        debug=application.config.get('DEBUG')
    )
