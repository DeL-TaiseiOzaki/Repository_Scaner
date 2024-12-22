import streamlit as st
import tempfile
import git
import os
from pathlib import Path
from datetime import datetime 
from typing import List, Set, Optional
from config.settings import Settings
from core.file_scanner import FileScanner, FileInfo
from services.llm_service import LLMService
from main import DirectoryStructureScanner, MarkdownGenerator

class StreamlitFileWriter:
    def __init__(self, output_file: Path):
        self.output_file = output_file
    
    def create_markdown(self, files: List[FileInfo]) -> str:
        content = []
        for file_info in files:
            content.append(f"## {file_info.path}")
            content.append("------------")
            if file_info.content is not None:
                content.append(file_info.content)
            else:
                content.append("# Failed to read content")
            content.append("\n")
        return "\n".join(content)

# ページ設定
st.set_page_config(
   page_title="Repository Code Analysis",
   page_icon="🔍",
   layout="wide"
)

# スタイル設定
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .directory-structure {
        font-family: monospace;
        white-space: pre;
        background-color: #1e2329;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .download-section {
        background-color: #1e2329;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'repo_content' not in st.session_state:
    st.session_state.repo_content = None
if 'structure_md' not in st.session_state:
    st.session_state.structure_md = None
if 'content_md' not in st.session_state:
    st.session_state.content_md = None
if 'temp_dir' not in st.session_state:
    st.session_state.temp_dir = None
if 'llm_service' not in st.session_state:
    try:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            st.error("ANTHROPIC_API_KEY環境変数が設定されていません")
            st.stop()
        st.session_state.llm_service = LLMService(api_key)
    except Exception as e:
        st.error(str(e))
        st.stop()

# メインのUIレイアウト
st.title("🔍 リポジトリ解析システム")

# サイドバーの設定
with st.sidebar:
    st.subheader("📌 使い方")
    st.markdown("""
    1. GitHubリポジトリのURLを入力
    2. スキャン対象の拡張子を選択
    3. スキャンを実行
    4. ディレクトリ構造を確認
    5. 解析結果をダウンロード
    """)
    
    # スキャン対象の拡張子選択
    st.subheader("🔍 スキャン対象の選択")
    
    # プログラミング言語
    st.write("プログラミング言語:")
    prog_exts = {'.py', '.js', '.ts', '.java', '.cpp', '.hpp', '.c', '.h', '.go', '.rs'}
    selected_prog = {ext: st.checkbox(ext, value=True, key=f"prog_{ext}") 
                    for ext in prog_exts}
    
    # 設定ファイル
    st.write("設定ファイル:")
    config_exts = {'.json', '.yml', '.yaml', '.toml'}
    selected_config = {ext: st.checkbox(ext, value=True, key=f"config_{ext}") 
                      for ext in config_exts}
    
    # ドキュメント
    st.write("ドキュメント:")
    doc_exts = {'.md', '.txt'}
    selected_doc = {ext: st.checkbox(ext, value=True, key=f"doc_{ext}") 
                   for ext in doc_exts}

# URLの入力
repo_url = st.text_input(
   "GitHubリポジトリのURLを入力",
   placeholder="https://github.com/username/repository.git"
)

# スキャン実行ボタン
if st.button("スキャン開始", disabled=not repo_url):
    try:
        with st.spinner('リポジトリを解析中...'):
            # 選択された拡張子を集約
            selected_extensions = {ext for exts in [selected_prog, selected_config, selected_doc]
                                for ext, selected in exts.items() if selected}
            
            # 選択がない場合はデフォルトを使用
            if not selected_extensions:
                selected_extensions = Settings.DEFAULT_EXTENSIONS
            
            # MarkdownGeneratorを初期化
            generator = MarkdownGenerator(repo_url, selected_extensions)
            content_md, structure_md, files = generator.generate_markdowns()
            
            writer = StreamlitFileWriter(Path("dummy"))
            formatted_content = writer.create_markdown(files)
            
            st.session_state.content_md = formatted_content
            st.session_state.structure_md = structure_md
            st.session_state.repo_content = LLMService.format_code_content(files)
            
        st.success(f"スキャン完了: {len(files)}個のファイルを検出")
        
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")

# スキャン結果の表示とダウンロード
if st.session_state.structure_md and st.session_state.content_md:
    # ディレクトリ構造の表示
    st.subheader("📁 ディレクトリ構造")
    st.markdown(f'<div class="directory-structure">{st.session_state.structure_md}</div>', 
               unsafe_allow_html=True)
    
    # ダウンロードセクション
    st.subheader("📥 解析結果のダウンロード")
    st.markdown('<div class="download-section">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📁 ディレクトリ構造をダウンロード",
            data=st.session_state.structure_md,
            file_name=f"directory_structure_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
    
    with col2:
        st.download_button(
            label="📄 ファイル内容をダウンロード",
            data=st.session_state.content_md,
            file_name=f"repository_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)