import numpy as np
import pandas as pd
import unittest as ut
from pymatgen.core import Structure
from pymatgen.core.trajectory import Trajectory

from gulpy.parser.md import MolecularDynamicsParser


class TestNVT(ut.TestCase):
    def setUp(self):
        self.parser = MolecularDynamicsParser.from_file(
            "files/md/md.out", "files/md/md.trg"
        )

    def test_coords(self):
        frames = self.parser.get_coords()
        self.assertEqual(len(frames), 5)

        expected_frame_1 = np.array(
            [
                [-2.14134361e00, 3.65542237e00, 2.62703519e00],
                [4.16807401e00, 7.12087602e00, 2.63591706e00],
                [4.15239803e00, 3.33959824e-02, 2.65878109e00],
                [-4.16558341e00, 7.26472181e00, 1.81040239e-02],
                [2.07897103e00, 3.66167276e00, -5.80916547e-02],
                [8.26118794e00, 4.76837026e-02, 1.06081561e-03],
                [8.31024323e00, 1.53498536e-02, 2.59592568e00],
                [2.08079830e00, 3.75152594e00, 2.57093512e00],
                [-4.11086835e00, 7.14144009e00, 2.64980289e00],
                [4.24202325e00, 7.05976541e-02, 4.19166531e-02],
                [4.18094478e00, 7.19037567e00, 2.08055109e-02],
                [-1.99234948e00, 3.66883344e00, 3.58747956e-02],
                [-6.79354190e-02, 4.41529043e00, 3.92295858e00],
                [2.38509117e00, 8.55612379e00, 3.91349177e00],
                [-2.39297207e00, 8.53784744e00, 3.92724935e00],
                [6.22077428e00, 6.41751377e00, 1.34407090e00],
                [3.85448228e00, 2.25963832e00, 1.33073992e00],
                [8.63011708e00, 2.25940835e00, 1.26172065e00],
                [-2.13615711e00, 5.93415571e00, 3.99786554e00],
                [2.08071001e00, 5.95413717e00, 3.97079326e00],
                [-3.44892126e-03, 9.66876205e00, 3.88204473e00],
                [8.39835022e00, 4.87550643e00, 1.25177923e00],
                [4.09244292e00, 4.85510735e00, 1.26419192e00],
                [6.27580998e00, 1.20822888e00, 1.30499652e00],
                [-1.57969864e00, 4.32868397e00, 3.99059168e00],
                [3.15777920e00, 7.22728068e00, 3.95940156e00],
                [-1.65728148e00, 9.94313041e00, 3.89099452e00],
                [7.82640417e00, 6.43911166e00, 1.30018540e00],
                [3.00796362e00, 3.62842570e00, 1.25020453e00],
                [7.87942494e00, 9.18162362e-01, 1.31574461e00],
                [1.61660142e00, 9.96238304e00, 3.88812892e00],
                [1.58675720e00, 4.43053821e00, 3.92743997e00],
                [-3.16949114e00, 7.16363050e00, 3.97958869e00],
                [4.63001768e00, 8.95620507e-01, 1.35029287e00],
                [4.69136298e00, 6.41868168e00, 1.36464777e00],
                [9.45000852e00, 3.59723089e00, 1.28650028e00],
                [-2.12859518e00, 3.69643734e00, 7.96328311e00],
                [4.22180821e00, 7.13520043e00, 7.86594739e00],
                [4.28493774e00, 2.51609435e-02, 7.94592593e00],
                [-4.21906691e00, 7.11697349e00, 5.21044334e00],
                [2.12134404e00, 3.59809547e00, 5.19242136e00],
                [8.30197467e00, -3.41985308e-02, 5.22719601e00],
                [8.24389612e00, -2.47034320e-02, 7.91296793e00],
                [2.02376887e00, 3.59088691e00, 7.83445803e00],
                [-4.15757330e00, 7.10880897e00, 7.80323101e00],
                [4.22600124e00, 9.52816522e-03, 5.29269982e00],
                [4.11935572e00, 7.17130621e00, 5.24837392e00],
                [-2.08312753e00, 3.59162539e00, 5.31352844e00],
                [1.28123956e-02, 4.53831018e00, 9.19271654e00],
                [2.42261522e00, 8.58871361e00, 9.22938107e00],
                [-2.40545603e00, 8.62056217e00, 9.21114750e00],
                [6.22029896e00, 6.22480122e00, 6.52782207e00],
                [3.82948767e00, 2.20140095e00, 6.50919311e00],
                [8.63594761e00, 2.20428510e00, 6.66506598e00],
                [-2.10613883e00, 6.03366722e00, 9.25514576e00],
                [2.18879299e00, 5.94276449e00, 9.17735831e00],
                [-3.51010354e-02, 9.62910742e00, 9.30953936e00],
                [8.37071076e00, 4.83138479e00, 6.53680873e00],
                [4.03765990e00, 4.80988819e00, 6.57519565e00],
                [6.25913413e00, 1.21861062e00, 6.49428499e00],
                [-1.53254635e00, 4.51123113e00, 9.23782601e00],
                [3.25025570e00, 7.22223695e00, 9.18086905e00],
                [-1.61175855e00, 1.00080476e01, 9.24306995e00],
                [7.77572141e00, 6.35405322e00, 6.51211078e00],
                [3.00318305e00, 3.54210184e00, 6.53862675e00],
                [7.87636245e00, 8.60436722e-01, 6.60691625e00],
                [1.64815042e00, 9.98188146e00, 9.27867966e00],
                [1.57666319e00, 4.41400341e00, 9.11312391e00],
                [-3.17646510e00, 7.25226832e00, 9.16771151e00],
                [4.67730062e00, 8.65101298e-01, 6.54384042e00],
                [4.65952215e00, 6.29435827e00, 6.56152809e00],
                [9.46532970e00, 3.58820500e00, 6.61026825e00],
                [-2.16666687e00, 3.70205595e00, 2.62451190e00],
                [4.14311592e00, 7.07405461e00, 2.63345542e00],
                [4.22031821e00, 3.21800381e-02, 2.65839792e00],
                [-4.13369466e00, 7.20175966e00, 1.73994062e-02],
                [2.10958914e00, 3.71406408e00, -5.80754247e-02],
                [8.20514685e00, 4.60916400e-02, -7.73413822e-05],
                [8.24729254e00, 1.30953586e-02, 2.59718385e00],
                [2.11121258e00, 3.79135014e00, 2.57703529e00],
                [-4.08557838e00, 7.09605039e00, 2.64841027e00],
                [4.29879865e00, 6.53530288e-02, 4.55251028e-02],
                [4.15357451e00, 7.13333316e00, 1.81311303e-02],
                [-2.03501251e00, 3.72539155e00, 3.31748903e-02],
                [-6.81312954e-02, 4.43083164e00, 3.92872763e00],
                [2.37588394e00, 8.55006233e00, 3.91549016e00],
                [-2.38590131e00, 8.53526498e00, 3.93218346e00],
                [6.21930947e00, 6.40970757e00, 1.34277060e00],
                [3.86769370e00, 2.26451032e00, 1.32525062e00],
                [8.62167769e00, 2.26474401e00, 1.26466118e00],
                [-2.18281612e00, 5.90799797e00, 3.99206090e00],
                [2.13069691e00, 5.92667211e00, 3.96557278e00],
                [-4.65159806e-03, 9.72145706e00, 3.88659668e00],
                [8.43932662e00, 4.90166688e00, 1.26143898e00],
                [4.04688427e00, 4.87899232e00, 1.27118784e00],
                [6.27713527e00, 1.15315595e00, 1.30238834e00],
                [-2.15121709e00, 3.74647167e00, 7.95703169e00],
                [4.18318164e00, 7.07516494e00, 7.86488950e00],
                [4.33240343e00, 2.39479436e-02, 7.94533849e00],
                [-4.18401887e00, 7.06009437e00, 5.21436432e00],
                [2.14799867e00, 3.66057822e00, 5.19928793e00],
                [8.24237493e00, -3.30369879e-02, 5.22532139e00],
                [8.18976130e00, -2.24400431e-02, 7.91464656e00],
                [2.06521453e00, 3.65361261e00, 7.83584657e00],
                [-4.13309361e00, 7.06580176e00, 7.80408564e00],
                [4.28609733e00, 1.56545926e-02, 5.28815451e00],
                [4.08774034e00, 7.11667113e00, 5.24790349e00],
                [-2.11986706e00, 3.64898687e00, 5.31069934e00],
                [1.17639586e-02, 4.54275242e00, 9.19062532e00],
                [2.41146376e00, 8.58274833e00, 9.23116453e00],
                [-2.39381893e00, 8.61068315e00, 9.21236562e00],
                [6.21869569e00, 6.22200733e00, 6.52781692e00],
                [3.83886775e00, 2.20729152e00, 6.50754106e00],
                [8.62036094e00, 2.21316354e00, 6.66144842e00],
                [-2.15387177e00, 6.00380414e00, 9.24557878e00],
                [2.22641904e00, 5.92404846e00, 9.17643934e00],
                [-3.64921081e-02, 9.69373228e00, 9.30064426e00],
                [8.41903370e00, 4.86020378e00, 6.54447756e00],
                [4.00393071e00, 4.83119424e00, 6.56901588e00],
                [6.25905591e00, 1.15598772e00, 6.50429651e00],
            ]
        )

        self.assertIsNone(np.testing.assert_almost_equal(frames[0], expected_frame_1))

    def test_velocities(self):
        frames = self.parser.get_velocities()
        self.assertEqual(len(frames), 5)

        expected_frame_1 = np.array(
            [
                [-1.95975904e00, -1.53774739e00, -1.16877274e00],
                [5.37959447e00, 6.82195635e-01, -1.82523421e00],
                [-4.05509799e-01, 1.88229589e00, 6.60573232e-01],
                [-3.24117145e00, -6.71805873e-01, -3.44245335e-02],
                [-3.03775914e-01, -1.05742607e00, -1.71442797e00],
                [2.15103079e-01, 1.22779963e00, 4.32981760e-02],
                [2.12063851e00, 3.41578311e-01, 2.20139492e00],
                [5.03820600e-01, -2.07817593e-02, 4.76385537e-01],
                [-2.38683157e00, 3.64206425e00, -7.62177338e-01],
                [6.31474080e-01, 2.09066905e-01, 6.04011127e-01],
                [4.45434203e00, -6.82317047e-01, -1.00757229e00],
                [2.44695452e00, 6.75691138e-01, -1.66908065e00],
                [2.77804532e00, 2.55483594e00, 2.57710106e00],
                [-8.32925591e-01, -4.18814611e-01, -6.00352421e-01],
                [1.26916516e00, -1.83882000e00, 1.56267537e00],
                [-1.04850772e00, -2.14351005e-01, 2.49428872e00],
                [1.36090149e00, 7.10593540e-01, -1.27565320e00],
                [-6.98909917e-01, 4.32941126e00, -1.41658904e00],
                [9.90878736e-03, -1.97311001e-02, 1.45855804e00],
                [-8.78800436e-01, 5.94961052e-01, -1.94647603e00],
                [-9.52779540e-02, -2.47681296e00, -1.34834216e00],
                [-4.48342430e00, -1.17016779e00, 2.89787079e00],
                [4.07194649e00, -1.07006979e00, 2.48558954e00],
                [1.53305162e00, -2.59943448e-01, -3.01581276e00],
                [-4.22471232e00, -1.10196678e01, 1.13432622e-01],
                [1.18808703e01, -1.75916439e00, 1.57967465e00],
                [-6.82501384e00, 7.27924312e00, 3.48749238e-01],
                [2.54596727e00, 9.10426787e00, 2.32153330e-01],
                [-9.83014690e00, -1.42911808e00, -1.31272405e00],
                [5.27127624e00, -7.67319358e00, -2.00341708e-01],
                [5.41027702e00, 5.65247237e00, -8.27173739e-01],
                [1.89610410e00, -8.40396499e00, -1.83151859e00],
                [-8.03666893e00, -6.84900379e-01, 1.02600281e-02],
                [-1.87460838e00, -6.40369845e00, -9.87954208e-01],
                [-5.10466803e00, 7.06571760e00, 5.00554830e-01],
                [5.39755755e00, 1.12765818e00, -6.20296861e-01],
                [6.16511188e00, 2.97571747e00, 4.16766146e00],
                [2.93246296e00, -4.08439761e00, -4.27482217e-01],
                [-3.82114728e00, 7.81634405e-03, 1.60236303e00],
                [-2.08625824e00, -1.72256223e00, 9.11123114e-01],
                [-4.87052077e-01, 1.57935295e00, 1.19549193e00],
                [3.95505369e-01, -6.10935018e-01, -1.88092140e00],
                [-7.73448112e-01, -1.14718029e00, 5.01440895e-03],
                [2.36077281e00, 1.12974270e00, -1.56156862e00],
                [-4.65536887e00, -1.55004675e00, -6.93902323e-01],
                [-1.08119889e00, 3.25309426e00, -4.72679280e-01],
                [1.69495041e00, -9.49578947e-01, 5.16678483e-01],
                [-1.10086977e00, 7.58674373e-01, -9.80928328e-01],
                [-4.87394946e00, 4.09224685e00, -1.96698044e00],
                [8.37050091e-02, -2.85607406e00, 4.87379274e-01],
                [1.10255519e00, -1.85424193e00, -1.84585653e00],
                [-3.15741818e00, -3.35386931e00, -6.63537791e-01],
                [2.40120225e00, 7.52985496e-02, -1.19981983e00],
                [-2.77298843e00, 2.92962412e00, 1.89379012e00],
                [2.50551065e00, -7.70631558e-01, -1.79767284e00],
                [-1.41428061e00, 3.85593349e00, -9.08756431e-01],
                [-3.98203133e00, 6.13287230e-01, 9.89261804e-01],
                [-3.37730973e-02, 1.65037526e00, 6.07005015e-01],
                [5.53851645e00, -1.64897187e-01, -1.71096289e00],
                [1.15132990e00, 1.37466433e00, 2.71548269e00],
                [-2.47594590e00, -9.66728831e00, 2.40527713e00],
                [1.20677277e01, 5.18170755e-01, -6.40326180e-02],
                [-7.53670684e00, 8.43026983e00, 1.83422611e00],
                [4.26139674e-01, 6.46799246e00, -5.48861828e-01],
                [-7.61668225e00, -1.81221045e00, -1.68533084e00],
                [8.46002952e00, -7.76952739e00, 9.79015307e-01],
                [4.25163136e00, 9.59644006e00, 2.78466603e00],
                [4.18083210e00, -7.22223590e00, -2.55864947e-01],
                [-1.09944462e01, 7.40271284e-01, -4.28012334e-01],
                [-6.16161199e00, -7.63661179e00, -1.25587570e00],
                [-3.54558199e00, 8.17225032e00, -1.25915310e00],
                [8.66456363e00, 1.37236415e00, 1.00380062e00],
                [-9.52991570e-01, -2.45070513e00, -1.25661394e00],
                [6.32767017e00, 1.63207533e00, -1.59356703e00],
                [-1.71222685e00, 2.26592955e00, 6.50354710e-01],
                [-3.72312637e00, 6.01771580e-01, -1.18728168e-02],
                [-1.31336770e00, -1.96781467e00, -1.63253984e00],
                [1.46075561e00, 1.75341534e00, 2.07208346e-01],
                [3.46674586e00, 1.59503578e-01, 2.10324993e00],
                [-5.00654888e-01, -8.08251397e-01, 9.51474172e-01],
                [-2.99987207e00, 4.82807777e00, -4.93212804e-01],
                [-7.14499858e-01, 2.63152084e-01, 4.03467867e-01],
                [5.44279408e00, 2.39242012e-01, -8.38811807e-01],
                [3.35887725e00, -3.27608499e-01, -1.54033504e00],
                [3.74798249e00, 3.22651227e00, 1.89676185e00],
                [-1.77336386e00, 3.90621608e-01, -1.16175916e00],
                [2.04159269e00, -2.74257035e00, 2.22703947e00],
                [-1.97860739e00, -6.26778092e-01, 1.58896713e00],
                [2.46455946e00, 2.52318744e-01, -6.22421275e-01],
                [-5.46757324e-01, 3.95226216e00, -2.71635702e00],
                [1.05829666e00, -8.83519989e-01, 1.55623233e00],
                [-1.71600703e00, 9.41344669e-02, -2.89676362e00],
                [1.07040087e00, -2.97921186e00, -8.54807094e-01],
                [-5.47041645e00, -3.63560595e-01, 2.41826681e00],
                [4.82145663e00, -1.20915651e00, 3.61416300e00],
                [4.75605585e-01, 3.35255617e-01, -3.63414486e00],
                [6.58036541e00, 1.75525810e00, 4.60678796e00],
                [3.84207242e00, -3.07199691e00, -4.76920191e-01],
                [-5.16986311e00, 1.88324804e-01, 1.54605184e00],
                [-3.07048541e00, -8.70189236e-01, 5.11691290e-01],
                [-8.14129718e-01, 2.68736853e-01, 1.02201484e00],
                [1.74556919e00, -7.40288882e-01, -1.75688948e00],
                [5.53719992e-01, -1.45175523e00, -2.04331221e-02],
                [1.74795358e00, -8.62930262e-02, -1.53924453e00],
                [-5.52478576e00, -5.02051145e-01, -7.18562258e-01],
                [-2.40684116e00, 3.50937355e00, -6.50954765e-01],
                [2.44144215e00, 1.80534784e-01, 6.59442932e-01],
                [-4.33463134e-01, -4.25459741e-01, -8.96173173e-01],
                [-4.53035225e00, 3.86269992e00, -6.69275615e-01],
                [2.08979276e-01, -4.20675613e00, 3.65917515e-01],
                [7.49808118e-01, -1.34513907e00, -6.32937553e-01],
                [-2.28277384e00, -3.98288615e00, 1.69603099e-01],
                [3.63624616e00, 2.99411331e-02, -1.77200677e00],
                [-2.88348543e00, 4.28037324e00, 2.02816228e00],
                [2.65544742e00, -3.02373177e-01, -5.27617058e-01],
                [-2.64592400e00, 4.43160728e00, -9.89023938e-01],
                [-4.83670520e00, -6.20752969e-02, 1.80670091e00],
                [-4.43131560e-01, 7.15916392e-01, 1.50922501e00],
                [5.71450356e00, -1.36520082e00, -1.09202156e00],
                [2.98045505e-01, 2.30459414e00, 2.20369666e00],
            ]
        )

        self.assertIsNone(np.testing.assert_almost_equal(frames[0], expected_frame_1))

    def test_site_energies(self):
        frames = self.parser.get_site_energies()
        self.assertEqual(len(frames), 5)

        expected_frame_1 = np.array(
            [
                13.60878194,
                13.74623039,
                13.84854051,
                13.32885395,
                13.72600251,
                14.07337935,
                13.72340406,
                13.74730858,
                13.32559691,
                13.6723109,
                13.25279265,
                13.46863071,
                14.1159037,
                14.37281688,
                14.18520667,
                14.15317977,
                13.9528495,
                14.6415009,
                13.29887792,
                13.69295571,
                13.41417889,
                13.25902804,
                13.10907775,
                13.4119407,
                -80.04138998,
                -79.79509024,
                -79.43954489,
                -80.65907699,
                -80.50710537,
                -79.66904882,
                -79.90994575,
                -79.86740512,
                -80.56963882,
                -80.06013919,
                -81.27078125,
                -80.03393794,
                13.6149515,
                13.62999434,
                13.46047403,
                13.77282686,
                13.93058577,
                13.11174915,
                13.66527511,
                14.09006912,
                13.40360167,
                13.38966184,
                13.37198187,
                14.16667037,
                14.44325918,
                13.97705696,
                14.05325188,
                14.33665547,
                14.13028649,
                14.28764053,
                13.83963022,
                13.32242936,
                13.08598078,
                13.40185102,
                13.88435426,
                13.60479007,
                -80.02509676,
                -80.13180493,
                -80.78049421,
                -80.60357316,
                -79.35351165,
                -79.71248769,
                -79.92868496,
                -79.83752742,
                -79.6707392,
                -80.31185243,
                -79.92522335,
                -79.39301793,
                -37.56800161,
                -37.62632182,
                -38.29565247,
                -37.160939,
                -37.74206627,
                -38.40488306,
                -38.07775785,
                -37.75602476,
                -36.82154485,
                -37.58537381,
                -36.7643446,
                -37.35388123,
                -38.20190309,
                -38.80569664,
                -38.56289471,
                -38.01962251,
                -37.96647952,
                -39.26834493,
                -37.18195637,
                -38.1186283,
                -37.78679162,
                -37.27206369,
                -36.7108323,
                -37.60795214,
                -37.81700003,
                -37.78035365,
                -37.34748694,
                -37.76732562,
                -38.37442104,
                -36.91912774,
                -37.88839665,
                -38.79888719,
                -37.36517526,
                -37.22247,
                -37.27966973,
                -38.93507581,
                -38.77605336,
                -38.20223665,
                -38.16931841,
                -38.51929878,
                -38.30129322,
                -38.74919568,
                -38.42416453,
                -37.41050846,
                -36.83681596,
                -37.44833907,
                -38.56068758,
                -37.98453105,
            ]
        )

        self.assertIsNone(np.testing.assert_almost_equal(frames[0], expected_frame_1))

    def test_step_props(self):
        steps = self.parser.get_step_props()
        self.assertEqual(len(steps), 5)
        self.assertIsInstance(steps, pd.DataFrame)

        expected = [
            0.600000000000007e-01,
            3.80326930055334,
            -3079.93053082179,
            414.413730559957,
        ]

        for x, y in zip(expected, steps.iloc[0, :].values):
            self.assertAlmostEqual(x, y)

    def test_trajectory(self):
        traj = self.parser.get_pymatgen_trajectory()
        self.assertEqual(len(traj), 5)
        self.assertIsInstance(traj, Trajectory)

    def test_len(self):
        self.assertEqual(len(self.parser), 5)

    def test_md_props(self):
        traj = self.parser.get_md_props()
        self.assertEqual(len(traj), 5)
        self.assertIsInstance(traj[0], dict)


class TestNPT(ut.TestCase):
    def setUp(self):
        self.parser = MolecularDynamicsParser.from_file(
            "files/md/npt.out", "files/md/npt.trg"
        )

    def test_cell(self):
        frames = self.parser.get_md_cell()
        self.assertEqual(len(frames), 5)

        expected = np.array(
            [
                [1.22173416e01, -6.65624849e-03, -7.86651887e-02],
                [-6.11433454e00, 1.05818581e01, -2.26421415e-03],
                [-6.23993662e-02, -3.81284426e-02, 1.04873166e01],
            ]
        )

        self.assertIsNone(np.testing.assert_almost_equal(frames[0], expected))


if __name__ == "__main__":
    ut.main()
