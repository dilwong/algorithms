import setuptools

if __name__ == "__main__":

    with open('requirements.txt', 'r') as f:
        requirements = f.readlines()
        requirements = [line.strip() for line in requirements if line.strip()]

    setuptools.setup(name = 'algorithms',
    version = '1.0.2',
    author = 'Dillon Wong',
    author_email = '',
    description = 'Basic algorithms and data structures',
    url = 'https://github.com/dilwong/algorithms',
    install_requires = requirements,
    packages=['algorithms'],
    package_dir={'algorithms': 'python'}
    )