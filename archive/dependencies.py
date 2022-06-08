import subprocess

def git(*args):
    return subprocess.check_call(['git'] + list(args))

git("clone", "https://github.com/CoolProp/CoolProp", "--recursive")