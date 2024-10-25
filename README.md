# simple-captcha-solver
Proeject to solve simple captchas like: 

![captcha image](example.jpg "Captcha example")

To build container with all requirements:

```sh
docker build -t captcha-solver:latest . --no-cache
```

To run the builded container with the code:

```sh
docker run --rm -it --name=captcha_solver --entrypoint bash captcha-solver:latest 
```

To run the script with example code:
```sh
python3 captcha.py
```