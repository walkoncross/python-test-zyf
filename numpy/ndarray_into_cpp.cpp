#include <boost/python/numpy.hpp>
#include <iostream>

namespace p = boost::python;
namespace np = boost::python::numpy;

int main(int argc, char **argv)
{
    Py_Initialize();
    np::initialize();
    int arr[] = {1, 2, 3, 4, 5};
    np::ndarray py_array = np::from_data(arr, np::dtype::get_builtin<int>(),
                                         p::make_tuple(5),
                                         p::make_tuple(sizeof(int)),
                                         p::object());
    std::cout << "C++ array :" << std::endl;
    for (int j = 0; j < 4; j++)
    {
        std::cout << arr[j] << ' ';
    }

    std::cout << std::endl
              << "Python ndarray :" << p::extract<char const *>(p::str(py_array)) << std::endl;
    py_array[1] = 5;

    std::cout << "Is the change reflected in the C++ array used to create the ndarray ? " << std::endl;
    for (int j = 0; j < 5; j++)
    {
        std::cout << arr[j] << ' ';
    }

    arr[2] = 8;
    std::cout << std::endl
              << "Is the change reflected in the Python ndarray ?" << std::endl
              << p::extract<char const *>(p::str(py_array)) << std::endl;
}