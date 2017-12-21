from setuptools import setup, Extension
from Cython.Build import cythonize

cggc_rg_wrap = Extension('pycggcrg.cggc_rg',
                         sources=['pycggcrg/cggc_rg.pyx',
                                  'cggc_rg/graph.cpp',
                                  'cggc_rg/partition.cpp',
                                  'cggc_rg/modoptimizer.cpp',
                                  'cggc_rg/activerowset.cpp',
                                  'cggc_rg/sparseclusteringmatrix.cpp',
                                  ],
                         include_dirs=['pycggcrg', 'cggc_rg'],
                         extra_compile_args=[],
                         language='c++')

setup(
    name='pycggcrg',
    version='0.2.4b0',
    packages=['pycggcrg'],
    url='https://github.com/FabianBall/pycggcrg',
    license='TODO',
    author='Fabian Ball',
    author_email='fabian.ball@kit.edu',
    description='Python wrapper for the CGGC-RG algorithm family',
    install_requires=['Cython'],
    ext_modules=cythonize(cggc_rg_wrap),
    test_suite='nose.collector',
    tests_require=['nose'],
    include_package_data=True,
)
