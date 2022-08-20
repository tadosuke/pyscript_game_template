# PyScript用ゲームテンプレート
PyScriptでゲームを作るためのひな形です。

## 使い方
src以下にあるファイル一式を同じフォルダ以下に置いて、ブラウザでindex.htmlを開くと実行できます。

![2022-08-20_10h15_10](https://user-images.githubusercontent.com/111171661/185723753-c43478d2-a08b-4397-90da-8f7798d9c53c.png)

各機能の簡単なサンプルが実装してあります。

主にmodel, viewの中身を書き換えてご利用ください。

## 設計

「pyscript_」と名前のついているモジュールはブラウザ以外では動作しません。  
（js、pyodideがブラウザ専用のため）

逆にそれ以外のモジュール（view.pyなど）はPyScriptに依存しないので、
ユニットテストを行ったり、PyScript以外の環境で作成したものを流用したりできます。

Viewは表示のみを行い、ViewからModelの操作は行いません。
Modelの操作はOperationメソッドなどから行われます。
