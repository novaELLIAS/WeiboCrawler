# WeiboCrawler

Assignment for Python courses, BUPT 2021.

## Dependencies

1. `Python 3.6`
2. `BeautifulSoup4`
3. `jieba`
4. `PIL`
5. `wordcloud`

## Functions

### `get_user_info(user_id: str)`

获取用户信息并存储到`result/userinfo.txt`中.

``` plain
name: 名字
desc: 描述
gender: 性别
followers: 粉丝数
follow: 关注数
```

### `get_content_last10(user_id: str, cont_id: str)`

获取最新10条动态并保存. 这不重要.

### `get_content_all(user_id: str)`

爬取id为`user_id`的用户的所有动态, 并以`txt`和`csv`格式保存.

大体流程: 获取容器列表 -> 爬容器信息 -> 文中有"阅读全文"? (改道爬原文):(直接塞进去) -> 去掉各种`HTML`标签 -> 存

### `get_containerid(url)`

获取容器id, 在`get_content_all(user_id: str)`有用.

### `get_full_content(contori: str) -> str`

获取全文, 在`get_content_all(user_id: str)`有用.

就正常爬就行了. 其实可以整个IP代理. 有的地方直接爬爬不到, 加上`cookie`就好了.

有遇到过编码问题. 直接大力`.encode('utf-8').decode('utf-8')`解决.

### `date_cleanup(start: datetime, end: datetime)`

数据清洗, 提取某时段的数据. 存起来.

### `generate_wordcloud()`

生成词云, 存起来. 因为背板形状不好, 所以效果不好. 这里只展示了一张正常生成的, 所有结果在`/result/`里面

![2021.05.04](https://cdn.jsdelivr.net/gh/novaELLIAS/WeiboCrawler/result/cleanup/wordcloud.jpg)

### Future Optimize

如果只需要一定时间段的数据, 貌似可以把配额从`O(n)`减少到`O(logn)`. 首先倍增来看到底有多少页数据, 然后对页二分拿到首尾, 然后爬一遍就行了.

## Statistics

![LICENSE](https://img.shields.io/github/license/novaELLIAS/WeiboCrawler)
![issues](https://img.shields.io/github/issues/novaELLIAS/WeiboCrawler)
![top language](https://img.shields.io/github/languages/top/novaELLIAS/WeiboCrawler)
![main.cpp size](https://img.shields.io/github/size/novaELLIAS/WeiboCrawler/main.py?label=main.py)
![repo size](https://img.shields.io/github/repo-size/novaELLIAS/WeiboCrawler?label=repo%20size)
![repo size](https://img.shields.io/github/commit-activity/m/novaELLIAS/WeiboCrawler)