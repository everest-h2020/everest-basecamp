Synthesis flow setup guide
=========================

Download a pre-built AppImage executable for Bambu:

```
wget https://release.bambuhls.eu/bambu-2024.1-dev.AppImage
chmod +x bambu-*.AppImage
ln -sf $PWD/bambu-*.AppImage ./bambu
ln -sf $PWD/bambu-*.AppImage ./mlir-opt-12
ln -sf $PWD/bambu-*.AppImage ./mlir-translate-12
export PATH=$PATH:$PWD
```

Make sure to have a supported simulator (Verilog or Modelsim) and logic synthesis toolchain (e.g. Vivado from Xilinx) if you intend to use the `--simulate` or `--evaluation` options.