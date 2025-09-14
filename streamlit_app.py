import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import random

# ページ設定
st.set_page_config(
    page_title="データの尺度水準",
    page_icon="📊",
    layout="wide"
)

# ページ選択をメインエリアに配置
st.title("データの尺度水準（pp.12-13）")
# タブでページ選択
tab1, tab2, tab3, tab4, tab5 = st.tabs(["基本概念", "詳細解説", "実践例", "クイズ", "データ分析体験"])

st.markdown("---")

# セッション状態の初期化
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_total' not in st.session_state:
    st.session_state.quiz_total = 0

def display_basic_concepts():
    """基本概念のページ"""
    st.header("📚 尺度水準学習Webアプリケーション")
    st.caption("Created by Dit-Lab.(Daiki ITO) ")
    st.caption("Supported by Tomoaki ATSUMI")
    
    st.markdown("""
    ## 尺度水準とは？
    
    尺度水準（測定水準）とは、データの性質を分類する概念です。
    統計学において、データの特性を理解し、適切な分析手法を選択するために重要です。
    """)
    
    # 4つの尺度水準の概要
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔢 量的データ")
        
        st.info("""
        **比率尺度（Ratio Scale）**
        - 絶対的な0点を持つ
        - 四則演算すべて可能
        - 例：身長、体重、年収
        """)
        
        st.success("""
        **間隔尺度（Interval Scale）**
        - 等間隔だが絶対的な0点なし
        - 加法・減法可能
        - 例：温度（℃）、偏差値
        """)
    
    with col2:
        st.subheader("📝 質的データ")
        
        st.warning("""
        **順序尺度（Ordinal Scale）**
        - 順序・大小関係あり
        - 間隔は不等
        - 例：成績（A・B・C）、満足度
        """)
        
        st.error("""
        **名義尺度（Nominal Scale）**
        - カテゴリーの分類のみ
        - 順序なし
        - 例：性別、血液型、職業
        """)
    
    # 階層構造の表示
    st.subheader("📊 尺度水準の階層構造")

    # 階層構造を表で表示
    hierarchy_data = {
        '尺度水準': ['比率尺度', '間隔尺度', '順序尺度', '名義尺度'],
        '持つ性質': [
            '分類・順序・等間隔・絶対零点',
            '分類・順序・等間隔',
            '分類・順序',
            '分類'
        ],
        '具体例': [
            '身長、体重、年収',
            '温度(℃)、偏差値',
            '成績、満足度',
            '性別、血液型'
        ],
        '可能な統計処理': [
            'すべての統計処理',
            '平均値、分散（比は不可）',
            '中央値、順位相関',
            '最頻値、カイ二乗検定'
        ]
    }

    hierarchy_df = pd.DataFrame(hierarchy_data)

    # スタイル付きの表を表示
    st.dataframe(
        hierarchy_df,
        use_container_width=True,
        hide_index=True
    )

    st.info("💡 **階層の特徴**: 上位の尺度ほど多くの統計的操作が可能で、比率尺度は最も情報量が多い尺度です。")

def display_detailed_explanation():
    """詳細解説のページ"""
    st.header("🔍 尺度水準の詳細解説")
    
    # タブで各尺度を詳しく説明
    tab1, tab2, tab3, tab4 = st.tabs(["名義尺度", "順序尺度", "間隔尺度", "比率尺度"])
    
    with tab1:
        st.header("📛 名義尺度（Nominal Scale）")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### 特徴
            - **分類**のみ可能
            - 数値に**順序の意味がない**
            - カテゴリーの**識別**が目的
            
            ### 可能な統計処理
            - 度数分布
            - 最頻値（モード）
            - カイ二乗検定
            
            ### 不可能な統計処理
            - 平均値、中央値
            - 四則演算
            - 分散、標準偏差
            """)
        
        with col2:
            st.subheader("具体例")
            examples = {
                "性別": ["男性", "女性", "その他"],
                "血液型": ["A型", "B型", "AB型", "O型"],
                "職業": ["会社員", "学生", "自営業", "その他"],
                "居住地": ["東京", "大阪", "名古屋", "福岡"]
            }
            
            for category, items in examples.items():
                st.write(f"**{category}**")
                for item in items:
                    st.write(f"• {item}")
                st.write("")
    
    with tab2:
        st.header("📊 順序尺度（Ordinal Scale）")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### 特徴
            - **順序・大小関係**がある
            - 間隔は**等しくない**
            - ランキングが可能
            
            ### 可能な統計処理
            - 度数分布
            - 最頻値（モード）
            - 中央値（メディアン）
            - 順位相関
            
            ### 不可能な統計処理
            - 平均値（厳密には）
            - 四則演算
            - 分散、標準偏差
            """)
        
        with col2:
            st.subheader("具体例")
            examples = {
                "成績": ["A", "B", "C", "D", "F"],
                "満足度": ["非常に満足", "満足", "普通", "不満", "非常に不満"],
                "企業規模": ["大企業", "中企業", "小企業"],
                "競技順位": ["1位", "2位", "3位", "..."]
            }
            
            for category, items in examples.items():
                st.write(f"**{category}**")
                for item in items:
                    st.write(f"• {item}")
                st.write("")
    
    with tab3:
        st.header("🌡️ 間隔尺度（Interval Scale）")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### 特徴
            - **等間隔**の目盛り
            - **絶対的な0点がない**
            - 差の比較が可能
            
            ### 可能な統計処理
            - 度数分布
            - 最頻値、中央値、平均値
            - 加法・減法
            - 分散、標準偏差
            - 相関係数
            
            ### 不可能な統計処理
            - 乗法・除法（比の計算）
            - 幾何平均
            """)
        
        with col2:
            st.subheader("具体例")
            examples = {
                "温度（℃）": ["0℃", "10℃", "20℃", "30℃"],
                "偏差値": ["30", "50", "70", "80"],
                "西暦": ["2020年", "2021年", "2022年", "2023年"],
                "知能指数": ["90", "100", "110", "120"]
            }
            
            for category, items in examples.items():
                st.write(f"**{category}**")
                for item in items:
                    st.write(f"• {item}")
                st.write("")
    
    with tab4:
        st.header("📏 比率尺度（Ratio Scale）")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### 特徴
            - **絶対的な0点**を持つ
            - **四則演算**すべて可能
            - 比の計算が意味を持つ
            
            ### 可能な統計処理
            - すべての統計処理が可能
            - 度数分布
            - 最頻値、中央値、平均値
            - 四則演算
            - 分散、標準偏差
            - 幾何平均、調和平均
            
            ### 注意点
            - 最も情報量が多い
            - 適切な分析手法を選択可能
            """)
        
        with col2:
            st.subheader("具体例")
            examples = {
                "身長（cm）": ["150", "160", "170", "180"],
                "体重（kg）": ["50", "60", "70", "80"],
                "年収（万円）": ["300", "400", "500", "600"],
                "時間（分）": ["0", "30", "60", "90"]
            }
            
            for category, items in examples.items():
                st.write(f"**{category}**")
                for item in items:
                    st.write(f"• {item}")
                st.write("")

def display_practical_examples():
    """実践例のページ"""
    st.header("💡 実践例とデータ分析")
    
    st.markdown("""
    ## 実際のデータセットで尺度水準を確認してみましょう
    """)
    
    # サンプルデータの作成
    np.random.seed(42)
    n_samples = 100
    
    sample_data = pd.DataFrame({
        '学生ID': range(1, n_samples + 1),
        '性別': np.random.choice(['男性', '女性'], n_samples),
        '学年': np.random.choice(['1年', '2年', '3年', '4年'], n_samples),
        '成績': np.random.choice(['A', 'B', 'C', 'D'], n_samples, p=[0.2, 0.3, 0.3, 0.2]),
        '身長': np.random.normal(165, 10, n_samples).round(1),
        '体重': np.random.normal(60, 12, n_samples).round(1),
        '満足度': np.random.randint(1, 6, n_samples),
        '温度': np.random.uniform(15, 35, n_samples).round(1)
    })
    
    # データの表示
    st.subheader("📋 サンプルデータ")
    st.dataframe(sample_data.head(10))
    
    # 各変数の尺度水準を分析
    st.subheader("🔍 各変数の尺度水準分析")
    
    scale_analysis = {
        '学生ID': {'尺度': '名義尺度', '理由': '単純な識別番号のため'},
        '性別': {'尺度': '名義尺度', '理由': 'カテゴリーの分類のみ'},
        '学年': {'尺度': '順序尺度', '理由': '学年には順序がある'},
        '成績': {'尺度': '順序尺度', '理由': 'A > B > C > D の順序がある'},
        '身長': {'尺度': '比率尺度', '理由': '絶対的な0点があり、比の計算が可能'},
        '体重': {'尺度': '比率尺度', '理由': '絶対的な0点があり、比の計算が可能'},
        '満足度': {'尺度': '順序尺度', '理由': '順序はあるが等間隔ではない'},
        '温度': {'尺度': '間隔尺度', '理由': '等間隔だが絶対的な0点がない（℃の場合）'}
    }
    
    for var, info in scale_analysis.items():
        with st.expander(f"{var}: {info['尺度']}"):
            st.write(f"**理由**: {info['理由']}")
            
            # 該当する統計量を計算
            if info['尺度'] == '名義尺度':
                freq = sample_data[var].value_counts()
                st.write("**度数分布:**")
                st.bar_chart(freq)
                st.write(f"**最頻値**: {freq.index[0]}")
                
            elif info['尺度'] == '順序尺度':
                freq = sample_data[var].value_counts()
                st.write("**度数分布:**")
                st.bar_chart(freq)
                if var == '満足度':
                    st.write(f"**中央値**: {sample_data[var].median()}")
                    
            elif info['尺度'] in ['間隔尺度', '比率尺度']:
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**基本統計量:**")
                    st.write(f"平均値: {sample_data[var].mean():.2f}")
                    st.write(f"中央値: {sample_data[var].median():.2f}")
                    st.write(f"標準偏差: {sample_data[var].std():.2f}")
                
                with col2:
                    fig = px.histogram(sample_data, x=var, title=f"{var}の分布")
                    st.plotly_chart(fig, use_container_width=True)

def display_quiz():
    """クイズのページ"""
    st.header("🎯 理解度チェッククイズ")
    
    # クイズ問題のデータベース
    quiz_questions = [
        {
            "question": "次のうち、比率尺度に該当するのはどれですか？",
            "options": ["温度（℃）", "身長（cm）", "成績（A,B,C,D）", "性別"],
            "correct": 1,
            "explanation": "身長は絶対的な0点（0cm）があり、比の計算が可能なため比率尺度です。"
        },
        {
            "question": "名義尺度で計算可能な統計量はどれですか？",
            "options": ["平均値", "中央値", "最頻値", "標準偏差"],
            "correct": 2,
            "explanation": "名義尺度では分類のみ可能で、最頻値（モード）のみ計算できます。"
        },
        {
            "question": "「とても満足」「満足」「普通」「不満」「とても不満」の5段階評価は何尺度ですか？",
            "options": ["名義尺度", "順序尺度", "間隔尺度", "比率尺度"],
            "correct": 1,
            "explanation": "順序はありますが、各段階の間隔が等しいとは限らないため順序尺度です。"
        },
        {
            "question": "間隔尺度の特徴として正しいのはどれですか？",
            "options": ["絶対的な0点がある", "四則演算すべて可能", "等間隔の目盛りがある", "順序がない"],
            "correct": 2,
            "explanation": "間隔尺度は等間隔の目盛りがありますが、絶対的な0点はありません。"
        },
        {
            "question": "次のうち、順序尺度に該当するのはどれですか？",
            "options": ["血液型", "偏差値", "競技の順位", "年収"],
            "correct": 2,
            "explanation": "競技の順位は順序がありますが、1位と2位の差と2位と3位の差は等しくないため順序尺度です。"
        }
    ]
    
    # クイズ実行
    st.write("各問題に答えて、尺度水準の理解を深めましょう。")
    
    if st.button("新しいクイズを開始"):
        st.session_state.quiz_score = 0
        st.session_state.quiz_total = 0
        st.session_state.current_questions = random.sample(quiz_questions, 3)
        st.session_state.user_answers = {}
    
    if 'current_questions' in st.session_state:
        for i, q in enumerate(st.session_state.current_questions):
            st.subheader(f"問題 {i+1}")
            st.write(q["question"])
            
            answer = st.radio(
                "選択してください:",
                q["options"],
                key=f"q_{i}",
                index=None
            )
            
            if answer:
                st.session_state.user_answers[i] = answer
                
                if q["options"].index(answer) == q["correct"]:
                    st.success("✅ 正解！")
                    st.write(f"**解説**: {q['explanation']}")
                else:
                    st.error("❌ 不正解")
                    st.write(f"**正解**: {q['options'][q['correct']]}")
                    st.write(f"**解説**: {q['explanation']}")
            
            st.write("---")
        
        # 結果の表示
        if len(st.session_state.user_answers) == len(st.session_state.current_questions):
            correct_count = sum(1 for i, q in enumerate(st.session_state.current_questions) 
                               if st.session_state.user_answers.get(i) == q["options"][q["correct"]])
            
            st.subheader("📊 結果")
            st.write(f"正解数: {correct_count} / {len(st.session_state.current_questions)}")
            
            score_percentage = (correct_count / len(st.session_state.current_questions)) * 100
            
            if score_percentage >= 80:
                st.balloons()
                st.success("🎉 素晴らしい！よく理解できています！")
            elif score_percentage >= 60:
                st.info("👍 良い理解度です。もう少し復習してみましょう。")
            else:
                st.warning("📚 基本概念を復習することをお勧めします。")

def display_data_analysis():
    """データ分析体験のページ"""
    st.header("📈 データ分析体験")
    
    st.markdown("""
    ## 尺度水準に応じた適切な分析手法を体験してみましょう
    """)
    
    # データの準備
    np.random.seed(42)
    n = 200
    
    analysis_data = pd.DataFrame({
        '部署': np.random.choice(['営業', '開発', '人事', 'マーケティング'], n),
        '役職': np.random.choice(['部長', '課長', '主任', '一般'], n, p=[0.1, 0.2, 0.3, 0.4]),
        '満足度': np.random.randint(1, 6, n),
        '年齢': np.random.randint(22, 65, n),
        '年収': np.random.normal(500, 150, n).astype(int),
        '勤続年数': np.random.randint(1, 30, n)
    })
    
    # 分析対象の選択
    st.subheader("🎯 分析対象を選択")
    
    analysis_type = st.selectbox(
        "分析タイプを選択してください:",
        ["基本統計", "相関分析", "グループ比較", "分布分析"]
    )
    
    if analysis_type == "基本統計":
        st.subheader("📊 基本統計量")
        
        variable = st.selectbox(
            "変数を選択:",
            ['部署', '役職', '満足度', '年齢', '年収', '勤続年数']
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if variable in ['部署', '役職']:
                st.write("**名義・順序尺度の統計量**")
                freq = analysis_data[variable].value_counts()
                st.write(freq)
                
                fig = px.bar(x=freq.index, y=freq.values, 
                           title=f"{variable}の度数分布")
                st.plotly_chart(fig, use_container_width=True)
                
            else:
                st.write("**量的データの統計量**")
                desc = analysis_data[variable].describe()
                st.write(desc)
                
                fig = px.histogram(analysis_data, x=variable, 
                                 title=f"{variable}の分布")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**適用可能な統計手法**")
            
            if variable in ['部署']:
                st.info("""
                **名義尺度**
                - 度数分布
                - 最頻値
                - カイ二乗検定
                """)
            elif variable in ['役職', '満足度']:
                st.warning("""
                **順序尺度**
                - 度数分布
                - 最頻値、中央値
                - 順位相関
                - マン・ホイットニー検定
                """)
            else:
                st.success("""
                **比率尺度**
                - すべての統計量
                - 平均値、分散
                - 相関係数
                - t検定、分散分析
                """)
    
    elif analysis_type == "相関分析":
        st.subheader("🔗 相関分析")
        
        # 量的変数のみ選択
        numeric_vars = ['満足度', '年齢', '年収', '勤続年数']
        
        var1 = st.selectbox("変数1を選択:", numeric_vars)
        var2 = st.selectbox("変数2を選択:", [v for v in numeric_vars if v != var1])
        
        if var1 and var2:
            correlation = analysis_data[var1].corr(analysis_data[var2])
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.scatter(analysis_data, x=var1, y=var2, 
                               title=f"{var1} vs {var2}")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.metric("相関係数", f"{correlation:.3f}")
                
                if abs(correlation) > 0.7:
                    st.success("強い相関があります")
                elif abs(correlation) > 0.3:
                    st.info("中程度の相関があります")
                else:
                    st.warning("弱い相関です")
                
                st.write("**相関の解釈**")
                if correlation > 0:
                    st.write("正の相関：一方が増加すると他方も増加する傾向")
                else:
                    st.write("負の相関：一方が増加すると他方は減少する傾向")
    
    elif analysis_type == "グループ比較":
        st.subheader("👥 グループ比較分析")
        
        group_var = st.selectbox("グループ変数:", ['部署', '役職'])
        compare_var = st.selectbox("比較する変数:", ['満足度', '年齢', '年収', '勤続年数'])
        
        if group_var and compare_var:
            fig = px.box(analysis_data, x=group_var, y=compare_var,
                        title=f"{group_var}別の{compare_var}比較")
            st.plotly_chart(fig, use_container_width=True)
            
            # グループ別統計
            group_stats = analysis_data.groupby(group_var)[compare_var].agg(['mean', 'median', 'std'])
            st.write("**グループ別統計量**")
            st.dataframe(group_stats)
    
    elif analysis_type == "分布分析":
        st.subheader("📊 分布分析")
        
        var = st.selectbox("分析する変数:", ['満足度', '年齢', '年収', '勤続年数'])
        
        if var:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.histogram(analysis_data, x=var, nbins=20,
                                 title=f"{var}のヒストグラム")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.box(analysis_data, y=var,
                           title=f"{var}の箱ひげ図")
                st.plotly_chart(fig, use_container_width=True)
            
            # 分布の特徴
            st.write("**分布の特徴**")
            mean_val = analysis_data[var].mean()
            median_val = analysis_data[var].median()
            
            if abs(mean_val - median_val) / mean_val < 0.1:
                st.success("ほぼ正規分布に近い対称的な分布です")
            elif mean_val > median_val:
                st.info("右に偏った分布（正の歪み）です")
            else:
                st.info("左に偏った分布（負の歪み）です")

# メインの実行部分（タブ形式）
with tab1:
    display_basic_concepts()

with tab2:
    display_detailed_explanation()

with tab3:
    display_practical_examples()

with tab4:
    display_quiz()

with tab5:
    display_data_analysis()

# フッター
st.markdown("---")
with st.expander("📚 学習のポイント"):
    st.markdown("""
    1. **データの性質を理解**
       - まず何を測定しているかを考える

    2. **適切な分析手法の選択**
       - 尺度水準に応じた手法を使用

    3. **結果の解釈**
       - 統計量の意味を正しく理解

    4. **実践的な応用**
       - 実際のデータで練習
    """)