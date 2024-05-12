import argparse
from cshogi import HuffmanCodedPosAndEval, Board, BLACK, move16
from cshogi import CSA
import numpy as np
import os
import glob
from sklearn.model_selection import train_test_split


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csa-dir', type=str, required=True, help='Directory containing CSA files')
    parser.add_argument('--hcpe-train', type=str, required=True, help='Output file for training data')
    parser.add_argument('--hcpe-test', type=str, required=True, help='Output file for test data')
    parser.add_argument('--filter-moves', type=int, default=50)
    parser.add_argument('--filter-rating', type=int, default=3500)
    parser.add_argument('--test-ratio', type=float, default=0.1)
    args = parser.parse_args()

    csa_file_list = glob.glob(os.path.join(args.csa_dir, '**', '*.csa'), recursive=True)

    # ファイルリストをシャッフル
    file_list_train, file_list_test = train_test_split(csa_file_list, test_size=args.test_ratio)
    # TODO: This has to be done after removing invalid data

    hcpes = np.zeros(1024, HuffmanCodedPosAndEval)

    f_train = open(args.hcpe_train, 'wb')
    f_test = open(args.hcpe_test, 'wb')

    board = Board()
    for file_list, f in zip([file_list_train, file_list_test], [f_train, f_test]):
        kif_num = 0
        position_num = 0
        for filepath in file_list:
            for kif in CSA.Parser.parse_file(filepath):
                # 投了、千日手、宣言勝ちで終了した棋譜以外を除外
                if kif.endgame not in ('%TORYO', '%SENNICHITE', '%KACHI'):
                    continue
                # 手数が少ない棋譜を除外
                if len(kif.moves) < args.filter_moves:
                    continue
                # レーティングの低いエンジンの対局を除外
                if args.filter_rating > 0 and min(kif.ratings) < args.filter_rating:
                    continue

                # 開始局面を設定
                board.set_sfen(kif.sfen)
                p = 0
                try:
                    for i, (move, score, comment) in enumerate(zip(kif.moves, kif.scores, kif.comments)):
                        # 不正な指し手のある棋譜を除外
                        if not board.is_legal(move):
                            raise Exception()
                        hcpe = hcpes[p]
                        p += 1
                        # 局面はhcpに変換
                        board.to_hcp(hcpe['hcp'])
                        # 16bitに収まるようにクリッピングする
                        eval = min(32767, max(score, -32767))
                        # 手番側の評価値にする
                        hcpe['eval'] = eval if board.turn == BLACK else -eval
                        # 指し手の32bit数値を16bitに切り捨てる
                        hcpe['bestMove16'] = move16(move)
                        # 勝敗結果
                        hcpe['gameResult'] = kif.win
                        board.push(move)
                except:
                    print(f'skip {filepath}')
                    continue

                if p == 0:
                    continue

                hcpes[:p].tofile(f)

                kif_num += 1
                position_num += p

        print('kif_num', kif_num)
        print('position_num', position_num)


if __name__ == '__main__':
    main()
