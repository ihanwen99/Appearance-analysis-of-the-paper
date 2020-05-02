```bash
pip install -r requirements

cd scripts
sh train.sh
```

主要修改是把依赖中的 `PIL` 转换成了 `pillow`，还添加了新的需要的依赖。

并且里面略微有 `Pytorch ` 版本不同的地方进行了修改，现在可以直接运行了。