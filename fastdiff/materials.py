"""Materials contains useful information on materials"""

class Material():
    def __init__(self, d_spacings, two_thetas, I_fixs, hkls, color, codid, label):
        self.d_spacings = d_spacings
        self.two_thetas = two_thetas
        self.I_fixs = I_fixs
        self.hkls = hkls
        self.color = color
        self.codid = codid
        self.label = label

global SRM640d 
SRM640d = Material(     [3.13560, 1.92010, 1.63750, 1.35770, 1.24590, 1.10860, 1.04520, 1.04520],
                        [28.442, 47.304, 56.122, 69.132, 76.380, 88.029, 94.951, 94.951],
                        [999, 618, 350, 87, 124, 163, 69, 24],
                        [r'$\bar{1}\bar{1}\bar{1}$', r'$\bar{2}\bar{2}0$', r'$\bar{3}\bar{1}\bar{1}$', r'$\bar{4}00$', r'$\bar{3}\bar{3}\bar{1}$', r'$\bar{4}\bar{2}\bar{2}$', r'$\bar{5}\bar{1}\bar{1}$', r'$\bar{3}\bar{3}\bar{3}$'],
                        '#006c9e',
                        2104748,
                        'SRM640d')
            #d-spacing, 2theta, I-fix(?), miller index

global LMNOFd3m 
LMNOFd3m = Material(    [4.71460, 2.88710, 2.46210, 2.35730, 2.04150, 1.87340, 1.57150, 1.57150, 1.44350, 1.38030, 1.24530, 1.23110, 1.17870, 1.14350, 1.14350, 1.06310, 1.06310, 1.02070],
                        [18.807, 30.949, 36.464, 38.146, 44.336, 48.558, 58.703, 58.703, 64.503, 67.844, 76.423, 77.467, 81.615, 84.696, 84.696, 92.868, 92.868, 97.995],
                        [999, 6, 437, 107, 488, 91, 151, 16, 255, 107, 35, 48, 59, 14, 38, 22, 28, 30],
                        [r'$\bar{1}\bar{1}\bar{1}$', r'$\bar{2}\bar{2}0$', r'$\bar{3}\bar{1}\bar{1}$', r'$\bar{2}\bar{2}\bar{2}$', r'$\bar{4}00$', r'$\bar{3}\bar{3}\bar{1}$', r'$\bar{5}\bar{1}\bar{1}$', r'$\bar{3}\bar{3}\bar{3}$', r'$\bar{4}\bar{4}0$', 
                        r'$\bar{5}\bar{3}\bar{1}$', r'$\bar{5}\bar{3}\bar{3}$', r'$\bar{6}\bar{2}\bar{2}$', r'$\bar{4}\bar{4}\bar{4}$', r'$\bar{7}\bar{1}\bar{1}$', r'$\bar{5}\bar{5}\bar{1}$', r'$\bar{7}\bar{3}\bar{1}$', r'$\bar{5}\bar{5}\bar{3}$', r'$\bar{8}00$' ],
                        '#700000',
                        4002459,
                        r'LNMO Fd$\bar{3}$m')