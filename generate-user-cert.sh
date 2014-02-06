#!/bin/sh

USERNAME=$1
EMAIL=$2
BPWD=$3

PARAMS_FILE=/tmp/koji-cert-params.lst

usage ()
{
	echo -e "Запускать скрипт надо так:\n\n    $0 <имя пользователя> <e-mail> <пароль>\n"
	echo -e "Пароль можно сгенерировать например так\n$ pwgen\n"
}

if [ "$USERNAME" == "" ]; then
	usage
	exit 1
fi

if [ "$EMAIL" == "" ]; then
	usage
	exit 1
fi

if [ "$BPWD" == "" ]; then
	usage
	exit 1
fi

CURRENT_UID=`id -u`
if [ "$CURRENT_UID" != "0" ]; then
	echo "Ты не root! Стань root'ом и тогда запускай!"
#	exit 1
fi

pushd /etc/pki/koji
# Step 1. Replace cnf file
cp ssl.cnf ssl.cnf.original
sed -i "s|koji.russianfedora.ru|${USERNAME}|g" ssl.cnf
sed -i "s|info@russianfedora.ru|${EMAIL}|g" ssl.cnf

# Step 2. Run gen_user_certs
echo "Run cert files generator..."
./gen_user_certs.sh $USERNAME
#/usr/local/bin/generate_koji_user_certs_archive.sh ${USERNAME}

# Step 3. Make conf-file
if [ -f $PARAMS_FILE ]; then
	rm -rf $PARAMS_FILE
fi
echo "certname=${USERNAME}" >> $PARAMS_FILE
echo "certemail=${EMAIL}" >> $PARAMS_FILE
echo "cbpwd=${BPWD}" >> $PARAMS_FILE

# Step 4. Send e-mail
python /usr/local/share/serverreport/serverreport.py ${EMAIL}

# Step 5. Clean
mv ssl.cnf.original ssl.cnf
popd

