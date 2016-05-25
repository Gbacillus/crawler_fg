echo "input your choice:"
read var
if [ $var = "yes" ]   #在等号两边加空格
then
echo $var
echo "input is correct"
else
echo $var
echo "input error"
fi
