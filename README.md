---
title: Repository Scaner
emoji: 💻
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.39.0
app_file: app.py
pinned: false
license: apache-2.0
short_description: プログラミング関連ファイルを再帰的にスキャンし、内容を単一のテキストファイルにエクスポートするツールです。
---

# get_repository_info_by_llm

プログラミング関連ファイルを再帰的にスキャンし、内容を単一のテキストファイルにエクスポートするツールです。GitHubリポジトリまたはローカルディレクトリに対応しています。

## 機能

- GitHubリポジトリのクローンとスキャン
- ローカルディレクトリのスキャン
- 再帰的なファイル検索
- 主要なプログラミング言語ファイルの検出
- UTF-8/CP932エンコーディングの自動検出
- 結果のテキストファイル出力

## 必要条件

- Python 3.7以上
- Git（GitHubリポジトリをスキャンする場合）

## インストール

1. リポジトリをクローン
```bash
git clone [このリポジトリのURL]
cd directory-scanner
```

2. 必要なディレクトリを作成
```bash
mkdir output
```

## 使用方法

### コマンドライン
```bash
# GitHubリポジトリをスキャン
python main.py https://github.com/username/repository.git

# ローカルディレクトリをスキャン
python main.py /path/to/directory
```

### シェルスクリプトを使用
```bash
# スクリプトに実行権限を付与
chmod +x scan.sh

# GitHubリポジトリをスキャン
./scan.sh https://github.com/username/repository.git

# ローカルディレクトリをスキャン
./scan.sh /path/to/directory
```

## 出力形式

スキャン結果は `output` ディレクトリに保存され、以下の形式で出力されます：

```
#ファイルパス
path/to/file.py
------------
ファイルの内容
```

## スキャン対象

### 対象となるファイル拡張子
- Python (.py)
- JavaScript (.js)
- Java (.java)
- C/C++ (.c, .h, .cpp, .hpp)
- Go (.go)
- Rust (.rs)
- PHP (.php)
- Ruby (.rb)
- TypeScript (.ts)
- その他 (.scala, .kt, .cs, .swift, .m, .sh, .pl, .r)

### 除外されるディレクトリ
- .git
- __pycache__
- node_modules
- venv
- .env
- build
- dist
- target
- bin
- obj

## 注意事項

- GitHubリポジトリをスキャンする場合、一時的にローカルにクローンされます
- スキャン完了後、クローンされたリポジトリは自動的に削除されます
- 大きなファイルや特殊なエンコーディングのファイルは読み取れない場合があります