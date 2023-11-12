cd "$(dirname "$0")"

target_dir=$CONDA_PREFIX/share/gadgetron/config/recon_config

echo "target dir: " $target_dir

if [ -e "$target_dir" ]; then
    # if dir exists
    read -p "$target_dir \exists, press enter to delete, or any other key to exit " response

    # check input
    if [ "$response" = "" ]; then
        rm -rf "$target_dir"
        echo "$target_dir \033[32mdeleted\033[0m!"
    else
        echo "exit"
        exit 1
    fi
fi

ln -s $PWD/../ugad4fun/recon_config $target_dir
if [ $? -eq 0 ]; then
   echo "ugad4fun config files \033[32msuccessfully\033[0m linked to $target_dir"
else
   echo "link \e[31mfailed\033[0m"
fi