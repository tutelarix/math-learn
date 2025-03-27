@echo off

if [%1]==[] (
    echo Welcome! Select a proper target.
    goto :eof
)

if [%1]==[install_p310] (
    call :update_packages
    goto :install_p310
)

if [%1]==[install_p311] (
    call :update_packages
    goto :install_p311
)

if [%1]==[format] (
    goto :format
)

if [%1]==[lint] (
    goto :lint
)

if [%1]==[test] (
    goto :test
)

if [%1]==[all_checks] (
    call :format_check
    call :lint
    goto :test
)


@echo No such target. Select a proper target.
goto :eof

:update_packages
    python -m pip install --upgrade pip -v
    python -m pip install --upgrade setuptools wheel -v
    goto :eof

:install_p310
    python -m pip install -r resources\requirements.txt -v --extra-index-url https://download.pytorch.org/whl/cu124
    python resources\install_yolox.py
    python -m pip freeze
    goto :eof

:install_p311
    python -m pip install -r resources\requirements.txt -v --extra-index-url https://download.pytorch.org/whl/cu124
    python resources\install_yolox.py
    python -m pip freeze
    goto :eof

:format_check
    python -m black --line-length=100 --check -t py310 -t py311 --required-version 24 .
    goto :eof

:format
    python -m black --line-length=100 -t py310 -t py311 --required-version 24 .
    goto :eof

:lint
    @echo Checking code with Mypy.
    python -m mypy --config-file=resources/configs/mypy.ini .
    @echo Checking code with Pyflakes.
    python -m pyflakes .
    @echo Checking code with Pylint.
    python -m pylint --rcfile=resources/configs/.pylintrc --disable=C .
    goto :eof

:test
    python -m pytest -vv --durations=15 --cov-config=resources/configs/.coveragerc --cov=. tests
    goto :eof
