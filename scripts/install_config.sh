cd "$(dirname "$0")"

target_dir=$CONDA_PREFIX/share/gadgetron/config/recon_config
cp -r $PWD/../ugad4fun/recon_config $target_dir