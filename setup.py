from setuptools import find_packages, setup
from typing import List  

HYPHEN_E_DOT='-e .'#from requirements.py
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()#reads all the packages listed in the requirement.txt one by one
        requirements = [req.strip() for req in requirements if req.strip() != HYPHEN_E_DOT]
        #if HYPHEN_E_DOT in requirements:
            #requirements.remove(HYPHEN_E_DOT)#-e .connects back to the setup.py but we dont wanna include it here like other packages thus remove
    print("Final requirements:", requirements)
    return requirements

setup(
    name='mlproject',
    version='0.0.1',#replace with new versions
    author='RADHE',
    author_email='radhempandey@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')#calling get_requirements and giving the path of requirements.txt


)