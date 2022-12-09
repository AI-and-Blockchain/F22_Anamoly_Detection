MU = 0
SIGMA = 0
MUS = [
	8.98016104e-17,
	3.16674798e-17,
	-4.09647876e-17,
	6.55564026e-16,
]
SIGMAS = [
	[
		0.88354068, 
		0.26917869,
		0.09191854,
		-0.52125903
	],
    [
    	-0.07794098,
    	0.88336539,
    	-0.11494633,
    	0.08228995
    ],
    [
    	0.13266029,
    	-0.0647766,
    	1.00277886,
    	0.33900438
    ],
    [
    	-0.53521361,
    	-0.12604031,
    	0.36143942,
    	0.96771862
    ]
]
SCALER_MUS = [
	5.502220741056456,
	104917.41897618743,
	12.274041973813828,
	8.860290641457999
]
SCALER_SIGMAS = [
	7.054427631499825,
	391418.45899804303,
	4.846098041871643,
	6.946700908609921
]
EPSILON = 1e-13
ADDRESS_REGEX = r"^(0x)?[0-9a-f]{40}$"
CONTRACT_ADDRESS = "0xC1cDB80cB8A5bF5629eaE76f1c96F4B0fB69105e"
NODE_URL = "https://goerli.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161"
ABI = [
	{
		"name" : "detection",
		"type" : "function",
		"inputs" : [
			{
				"indexed" : True,
				"internalType" : "int128",
				"name" : "x0",
				"type" : "int128",
			},
			{
				"indexed" : True,
				"internalType" : "int128",
				"name" : "x1",
				"type" : "int128",
			},
			{
				"indexed" : True,
				"internalType" : "int128",
				"name" : "x2",
				"type" : "int128",
			},
			{
				"indexed" : True,
				"internalType" : "int128",
				"name" : "x3",
				"type" : "int128",
			},
		],
		"outputs" : [
			{
				"internalType" : "bool",
				"name" : "",
				"type" : "bool",
			}
		],
		"stateMutability" : "view",
	}
]
FEATURES = [
	'from_benfords_second',
	'in_gas_limit_avg',
	'merged_benfords_second',
	'to_benfords_second',
]
DIGITS = 24