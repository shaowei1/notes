# lspci -v -s 00:02.0
fc000000 (32-bit, prefetchable) [size=32M]
	Memory at febf0000 (32-bit, non-prefetchable) [size=4K]
	Expansion ROM at febd0000 [disabled] [size=64K]
	Kernel driver in use: cirrus
	Kernel modules: cirrus

# lspci | grep NVIDIA

# connect aws by public key

sudo ssh -i libo.pem ubuntu@domain
