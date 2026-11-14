import sys

def patch_file(path, old, new):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if old not in content:
        print(f"ERROR: Could not find target pattern in {path}")
        sys.exit(1)
    content = content.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully patched {path}")

# 1. Disable CRC packet drop and accept replacement LCD Chip ID 0x5252
patch_file(
    "linux/drivers/input/touchscreen/ft8756.c",
    "#define READ_CMD    (0x80 | DATA_CRC_EN)",
    "#define READ_CMD    0x80"
)
patch_file(
    "linux/drivers/input/touchscreen/ft8756.c",
    "if (chip_id != 0x5652 || ret) {",
    "if ((chip_id != 0x5652 && chip_id != 0x5252) || ret) {"
)

# 2. Add calibrated touchscreen-size to Device Tree
patch_file(
    "linux/arch/arm64/boot/dts/qcom/sm8250-xiaomi-alioth.dts",
    'compatible = "focaltech,ft8756-spi";',
    'compatible = "focaltech,ft8756-spi";\n\t\ttouchscreen-size-x = <1080>;\n\t\ttouchscreen-size-y = <2400>;'
)
