cmake_minimum_required(VERSION 3.21)
project(imagepassthroughgadget)
set(CMAKE_CXX_STANDARD 17)

set(NAME g4f_imagepassthroughgadget)
set(GADGETRON_INSTALL_CONFIG_PATH share/gadgetron/config)

find_package(Gadgetron REQUIRED)
find_package(cpr REQUIRED)
#find_package(ISMRMRD REQUIRED)

add_library(${NAME} SHARED imagepassthroughgadget.cpp)
target_link_libraries(${NAME} Gadgetron::gadgetron_core)

install(TARGETS ${NAME}
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib
        RUNTIME DESTINATION bin
        COMPONENT main
        )

install(FILES config/default_with_image_passthrough.xml  DESTINATION ${GADGETRON_INSTALL_CONFIG_PATH} COMPONENT main)