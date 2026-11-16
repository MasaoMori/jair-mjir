# jair-mjir — JAIR・MJIR 統合サイト(Hugo版)

## サイトの更新方法

投稿(お知らせ)やページを追加・修正して、`main` ブランチに反映すると、GitHub Actions が自動でサイトをビルドして公開する(数分かかる)。
更新の方法は2つ。ブラウザだけで済ませるなら**方法1**、公開前に画面で確認したい・複数ファイルをまとめて直したいなら**方法2**。
どちらも、原稿は「フォルダ + `index.md`」の形で作る(下の「記事ファイルの書き方」を参照)。画像やPDFは、同じフォルダに置く。

### 方法1: GitHub のページ(ブラウザ)で投稿する
パソコンに何も入れずにできる。ただし、**`main` に反映した時点で公開される**(公開前に画面で確認はできない)。確認したいときは、手順 5 で「新しいブランチを作る」を選ぶか、方法2を使う。

1. https://github.com/MasaoMori/jair-mjir を開き、`content/posts/`(投稿)または `content/pages/`(固定ページ)のフォルダへ移動する。
2. 右上の **Add file → Create new file** を押す。
3. 名前の欄に `mjir2027-call/index.md` と入力する。`/` を入れると、フォルダ(`mjir2027-call`)が自動で作られる。フォルダ名が公開URLの一部になる(英数字とハイフンがよい)。
4. 本文の欄に、front matter と本文を書く(書き方は下の「お知らせ(投稿)を追加する」)。
5. 右上の **Commit changes…** を押し、メッセージ(例: `お知らせ: MJIR2027 発表募集`)を書いて、**Commit directly to the `main` branch** を選んで **Commit changes**。
   - 公開前に確認したいときは、**Create a new branch for this commit and start a pull request** を選ぶ。プルリクエストが作られ、内容を確認してから **Merge pull request** で `main` に統合すると公開される。
6. 画像・PDFを添付するときは、手順 5 のあと、作ったフォルダ(`content/posts/mjir2027-call/`)を開き、**Add file → Upload files** でファイルをドラッグして、同じように Commit する(フォルダが無いうちはアップロードできないので、`index.md` を先に作る)。
7. 公開の進み具合は、リポジトリの **Actions** タブで見る。緑のチェックが付けば公開済み(https://jairweb.jp/ )。赤い × のときは、中を開いてエラーを確認する。

既存のページを直すときは、該当ファイルを開いて右上の鉛筆アイコン(Edit)を押し、同じように Commit する。

### 方法2: ローカルPCでブランチを作り、`main` に統合する
画面で確認してから公開できる。`main` を直接書き換えずに、作業用のブランチで作業する。

**初回だけ**(リポジトリをパソコンに取り込む。メディアが約300MBあるので少し時間がかかる)
```bash
git clone https://github.com/MasaoMori/jair-mjir.git
cd jair-mjir
```

**投稿のたびに**
```bash
# 1. main を最新にして、作業用ブランチを作る(ブランチ名は何でもよい)
git switch main
git pull
git switch -c post/mjir2027-call

# 2. フォルダを作り、index.md を書き、画像・PDFを同じフォルダに置く
mkdir content/posts/mjir2027-call
#   content/posts/mjir2027-call/index.md  を編集
#   content/posts/mjir2027-call/flyer.pdf などをコピー

# 3. 画面で確認する(止めるときは Ctrl+C)
hugo server --renderToMemory --noBuildLock
#   http://localhost:1313/ を開く。下書き(draft: true)も見るなら -D を付ける。
#   1313番が使用中なら  --port 1314 --baseURL http://localhost:1314/  を付ける。

# 4. 変更を記録して、GitHub に送る
git add content/posts/mjir2027-call
git commit -m "お知らせ: MJIR2027 発表募集"
git push -u origin post/mjir2027-call
```

**`main` に統合する**(どちらか1つ)

- **GitHub 上で統合する(おすすめ)**: `git push` のあと、GitHub のリポジトリのページに出る **Compare & pull request** を押す → 内容を確認して **Create pull request** → **Merge pull request** → **Confirm merge**。
- **パソコン上で統合する**:
  ```bash
  git switch main
  git pull
  git merge post/mjir2027-call
  git push
  ```

`main` に統合されると、GitHub Actions が自動で公開する(進み具合は **Actions** タブ)。公開できたら、作業用ブランチは消してよい。
```bash
git branch -d post/mjir2027-call              # パソコン上のブランチ
git push origin --delete post/mjir2027-call   # GitHub 上のブランチ(プルリクエストで統合したときは、統合の画面の Delete branch でもよい)
```

## 記事ファイルの書き方

### お知らせ(投稿)を追加する
`content/posts/` に、フォルダ名がそのまま公開URLの最後の部分になるフォルダを作り、その中に `index.md` を置く。

```
content/posts/mjir2027-call/
├── index.md        ← 原稿
├── flyer.pdf       ← 添付ファイル(同じフォルダに置く)
└── poster.jpg
```

`index.md` は次の形で書く。

```markdown
---
title: "MJIR2027 発表募集のお知らせ"
date: 2026-12-01
news_category: "mjir"
---

本文をここに書く。

![ポスター](poster.jpg)

[募集要項(PDF)](flyer.pdf)
```

- 公開URLは `/2026/12/01/mjir2027-call/`(日付は `date` から、最後はフォルダ名)になる。フォルダ名と違う名前にしたいときだけ、front matter に `slug: "別の名前"` を足す。
- **`date`** は公開日。`2026-12-01` のように**日付だけでよい**(日本時間の0時として扱われる)。公開URLの `/年/月/日/` と、画面の日付表示も、これで決まる。
  - 同じ日に複数の投稿があって並び順を決めたいときだけ、時刻まで書く(例: `2026-12-01T15:00:00+09:00`。末尾の `+09:00` を付ける)。新しい時刻のほうが上に出る。
  - **未来の日付の投稿は、その日が来るまで公開されない。ただし、サイトは `main` に反映(push)したときにしか作り直されないので、日付が来ても自動では公開されない。** 日付を過ぎたあとに、何か1つ反映すると公開される。予約投稿として使うなら、公開したい日に反映する。
- **`news_category`** はお知らせの分類で、`related`(関連情報)、`recruit`(公募情報)、`mjir`(MJIR)、`events`(イベント)から選ぶ。省略すると `related`。分類の追加・名前の変更は `data/news_categories.yml`。
- 投稿は、トップの「お知らせ」(最新10件)、`/news/`、投稿のアーカイブ、`/feed.xml` に**自動で**載る。一覧を手で直す必要はない。
- `layout` や `url` は書かない(投稿用のレイアウトは自動で使われる)。

### 固定ページを追加する
`content/pages/` に、フォルダ名が公開URLになるフォルダを作り、その中に `index.md` を置く。

```
content/pages/privacy/index.md   →  /privacy/
```

```markdown
---
title: "ページの題名"
nav_section: "about"
---

本文をここに書く。
```

- `nav_section` は、ヘッダーのメニューのどれを強調するかを決める。`about`(協会について)、`meetings`(研究活動)、`conference`(MJIR)、`members`(会員の方へ)、`membership`(入会案内)から選ぶ。省略してもよい。
- メニューやフッターに載せるリンクは `data/navigation.yml` を編集する。ページを作るだけではメニューには出ない。
- HTMLで組んだデザインページ(`/about/` や `/membership/` のような形)にしたいときは、`index.html` にして、front matter に `layout: "native"` を足す(`content/pages/about.html` を参考にする)。
- トップの見出し・MJIRの告知バナー・「日本IR協会について」・論文集の案内は `data/home.yml`。

### 画像・PDFを載せる
投稿やページのフォルダに、ファイルをそのまま置く。本文では**ファイル名だけ**で指す。

```markdown
![説明文](poster.jpg)
[募集要項(PDF)](flyer.pdf)
```

- ファイルは、そのページの公開URLの下(例: `/2026/12/01/mjir2027-call/flyer.pdf`)に公開される。
- 複数のページで使う画像や、サイト全体の画像は、`static/` に置いて `/` から始まるパスで指す(例: `/assets/img/xxx.png`)。公開URLのドメイン直下(`https://jairweb.jp/assets/img/xxx.png`)になる。
- サイト内のリンクも同じ書き方でよい(例: `[入会案内](/membership/)`)。

### 既存の投稿・ページを直す
旧サイトから移したものは、まだ平らなファイル(`content/posts/2012-08-13-mjir-371.md` など)で、公開URLは front matter の `url` で決めている。そのまま `content/posts/` または `content/pages/` の該当ファイルを開いて編集する。見つけにくいときは、題名や `url` で検索する。**公開URLは変えない**(旧URLからのリンクが切れるため)。
旧サイトの画像・PDFは `static/wp-content/uploads/` にあり、本文から `/wp-content/uploads/…` で指している。

## このサイトについて

日本インスティテューショナル・リサーチ協会(JAIR、jairweb.jp)と大学情報・機関調査研究会(MJIR、mjir.info)の公開コンテンツを1つの Hugo サイトにまとめたもの。
`jekyll-site` の Jekyll 版から変換した。GitHub Pages に独自ドメイン https://jairweb.jp/ で公開している(旧 `masaomori.github.io/jair-mjir/` は、独自ドメインに自動で転送される)。mjir.info は、別リポジトリ `mjir-redirect` で `https://jairweb.jp/conference/` に転送している。

- 内容: 投稿89件(`content/posts`)、固定ページ106件(`content/pages`)、メディア(`static/wp-content/uploads`)。
- 旧URL: Jekyll版と同じ。旧サイトから移したページは、front matter の `url` で公開URLを指定している。新しく作るページは `hugo.yaml` の `permalinks` で決まる(投稿は `/年/月/日/フォルダ名/`、固定ページは `/フォルダ名/`)。一覧ページ(`/posts/` など)や分類ページは作らない。
- 設定は `hugo.yaml`、ナビは `data/navigation.yml`、トップの手入力部分は `data/home.yml`、お知らせの分類は `data/news_categories.yml`。
- テンプレートは `layouts/`(`baseof` / `home` / `page` / `posts/page`(投稿)/ `native`(手書きHTMLのページ)、部品は `_partials/`、`_shortcodes/` はお知らせ一覧の差し込み用)。

## ローカルでの確認
```bash
hugo server                       # http://localhost:1313/
hugo                              # public/ に出力(baseURL は https://jairweb.jp/)
python3 -I scripts/verify.py public                     # 検証(ビルド後)
```
Hugo は 0.170.0 で確認(`HUGO_VERSION` は `.github/workflows/pages.yml`)。

## 公開
`main` への push で `.github/workflows/pages.yml` が Hugo をビルドして GitHub Pages に公開する。リポジトリの Settings → Pages の Source は「GitHub Actions」にしておく。

## Jekyll版からの変換
`scripts/convert_from_jekyll.py <jekyll-siteのパス>` が `content/`・`data/`・`static/` を作り直す(`layouts/` と `hugo.yaml` は手書きで、触らない)。**取り込みは済んでおり、通常は再実行しない。** 再実行すると、その後に追加・編集した内容が消えるので、`content/` があるときは `--force` を付けないと動かない。
Markdown の解釈が Jekyll(kramdown)と Hugo(goldmark)で違うため、変換時に次を補正している。
- `**太字**`、`***太字+斜体***`、`~~取り消し線~~` は、日本語の句読点・リンクの隣だと Hugo では効かないので、HTML(`<strong>` など)に直す。
- 文章の直後の `-----` は、直前の行が見出しになってしまうので、空行を入れて区切り線にする。

`hugo.yaml` の設定の意味:
- `security.allowContent`: Hugo 0.170 は既定で `.html` のコンテンツを拒否する。固定ページ10件が手書きHTMLなので許可している。
- `markup.goldmark.renderer.unsafe`: 本文中の生HTMLを出力する。
- `markup.goldmark.extensions.linkify: false`: 本文中の裸のURL・メールを自動リンクにしない(Jekyll版と同じ)。

## Jekyll版との差(確認済み)
全195ページをデプロイ済みのJekyll版と比べた(本文のHTMLを正規化して比較)。141ページは一致。残り54ページの差は、次の Markdown 解釈の違いによるもの。
- 行末の `\`(WordPress 変換由来の改行)を、Jekyll版は文字のまま表示、Hugo版は改行(`<br>`)にする。
- 番号付きリストの開始番号を Hugo は守る(`<ol start="3">`)。
- Hugo版は、HTML の `<div>` の中の `##` や `**` も Markdown として解釈する。
- コードブロックの HTML が違う(`<div class="highlight">` の有無)。
- お知らせ一覧で、同じ日時(2024-04-04 09:00)の2件の並びが逆。

## 旧サイトから引き継いだ未解決
次の6件のリンクはJekyll版でも404(元のWordPressサイトから切れていた)。
`/2013/07/27/〔速報〕mjir-irimプログラム！/`、`/2014/05/14/mjir2014発表・参加申込募集開始/`、`/2015/06/11/大学ir人材育成カリキュラム-岡山集中講習会/`、`/2019/10/16/第８回mjirプログラム発表/`、`/regist2013/`、`/wp-content/uploads/2024/12/5f82244114001aa030ecd25e8cb45840-2.pdf`
