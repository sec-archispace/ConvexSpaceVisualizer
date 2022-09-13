## Convex Space Visualizer

### はじめに
本ソフトウェアは、株式会社セックと東京大学生産技術研究所・本間裕大准教授による共同研究の成果物です。

『凸空間の列挙による建築空間の形態分析』の論文（参考1）に記される凸空間列挙アルゴリズムを実装したソフトウェアで、
様々な空間の平面形状（柱などの空洞を内包しないもの）を入力として、凸空間列挙に基づく空間特性を可視化できます。

本共同研究は、株式会社セックと国立大学法人東京大学が締結した共同研究契約に基づきます。

### フォルダ構成
<pre>
ConvexSpaceVisualizer
│  main.py
│  README.md
│  LICENSE.txt
│  
├─contents
│      main.pyから利用されるファイル群
│      
├─convexspaceheatmap
│  │  convexspaceheatmap.jar
│  │  
│  ├─mace
│  │      mace.exe または mace を置くフォルダ
│  │      
│  ├─polygons
│  │      main.pyから操作されるフォルダ
│  │      
│  └─properties
│          enumeration.properties
│          visualization.properties
│          
├─polygons
│      頂点リストが保存されるフォルダ
│      
└─properties
        messages_eng.json
        messages_jpn.json

</pre>

### 事前準備
#### python・pythonライブラリのインストール
 - python3.8.0以上のpythonをインストールし、pathを通す。
 - tkパッケージ（入っていなければ）、Pillow パッケージをインストールする。
   -  コマンド例）
      ```
      pip install Pillow
      ```

#### javaのインストール
openjdk-16以上のJavaをインストールし、pathを通す。

#### mace実行ファイルの作成
##### Windowsの場合
1. makeのためのプログラムを取得する
    1. make for Windows
        1. 以下のURLにアクセスする
            http://gnuwin32.sourceforge.net/packages/make.htm
        1. 「Download」 の「Complete packages, except sources」の右横の 「Setup」をクリックし、exeファイルをダウンロードする
        1. ダウンロードしたexeファイルをダブルクリックしすべて標準でインストールする
        1. Pathにmake for Windowsを追加する
            1. スタートメニュー > 設定 > 詳細情報 > システムの詳細設定を開き、詳細設定のタブの環境変数ボタンを押下する
            1. システム環境変数から『Path』を選択し、編集ボタンを押下する
            1. 新規ボタンを押下し、以下の文字列を追加する。
            ```
            C:\Program Files (x86)\GnuWin32\bin
            ```
            1. OKを押下して開いたウインドウを閉じる

    2. mingw-w64
        1. 以下のURLにアクセスし、『MingW-W64-builds』を押下する
          https://www.mingw-w64.org/downloads/
        1. Mingw-buildsの見出しのInstallation: GitHubのリンクからGitHubにアクセスする
        1. Assetsという見出しの部分で、環境にあったファイルをダウンロードする（64bit環境→x86_64、32bit環境→i686から始まるファイルをダウンロード）
        1. ダウンロードしたファイルを任意のフォルダに展開する
        1. 展開したフォルダの『mingw32\bin』フォルダのフルパスをPathに追加する
            1. path追加手順は上記make for Windowsを参照

1. 以下のURLから『MACE』のプログラムソースコードを取得し、任意のフォルダに展開する。
  『宇野毅明と有村博紀による公開プログラム（コード）』
  http://research.nii.ac.jp/~uno/codes-j.htm
1. コマンドプロンプトを開き、『MACE』プログラムを展開したフォルダに移動する。
1. 以下のコマンドを実行し、生成されたmace.exeファイルをフォルダ構成の『convexspaceheatmap\mace』 配下に配置する。
    ```
    make
    ```

##### Macの場合
1. 以下のURLから『MACE』のプログラムソースコードを取得し、任意のフォルダに展開する。
  『宇野毅明と有村博紀による公開プログラム（コード）』
  http://research.nii.ac.jp/~uno/codes-j.htm
1. 端末アプリを開き、『MACE』プログラムを展開したフォルダに移動する。
1. 以下のコマンドを実行する。
    ```
    make
    ```

    ※『コマンドライン・デベロッパーツール』がインストールされていない場合、インストールし、再度makeコマンドを実行する

1. 生成されたmaceファイルをフォルダ構成の『canvas\convexspaceheatmap\mace』 配下に配置する。
1. 配置したmaceファイルに実行権限を付与する。


### 起動方法
1. コマンドを実行するウインドウを開き、main.pyを配置したフォルダに移動する。
1. main.pyを実行する。  
コマンド例）
    ```
    python3  main.py
    ```

### 動作確認環境
 - Windows 10
 - MacOS 10.15
 - python
   - 3.8.10(tkパッケージ込みでインストール)
   - Pillow 8.1.0, 
 - java
   - 16.0.1

### convexspaceheatmap.jar に関する利用規約
1. ソフトウェアの使用については許諾しますが、ソフトウェアに関連する著作権は著作者に帰属します。
1. アカデミック利用に限ります。商用目的の利用は禁止します。
1. 本ソフトウェアが出力した内容を利用する場合は出典元として本ソフトウェアおよび参考論文(参考1)を表記してください。
1. 出力した内容について、著作者は責任を負いません。
1. 改変、翻案は禁止します。
1. 再配布は禁止します。

### 上記以外の公開物のライセンス
MIT License

### 参考
1. 野畑剛史, 本間裕大, 今井公太郎: 『凸空間の列挙による建築空間の形態分析』, 日本建築学会計画系論文報告集, No.766, pp.2545--2552, 2019
https://doi.org/10.3130/aija.84.2545
1. 『宇野毅明と有村博紀による公開プログラム（コード）』（閲覧日：2022/09/05）
http://research.nii.ac.jp/~uno/codes-j.htm 


以上
