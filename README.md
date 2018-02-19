# Telkom Balance

Get notification every hour on your airtime balance, data bundle balance and extras as acquired from the [customer portal](http://myaccount.telkom.co.ke).

# Usage

## Install requirements

`$ pip install -r requirements.txt`

## Edit config file

>Edit the sample [defaults.ini](sampledefaults.ini) appropriately:


>> 1. Rename it to `defaults.ini`
>>
>> 2. Change the value of `driverspath` to the location of the downloaded drivers
>>
>> 3. Enter the file name of the driver (either at `chromedrivername` or `firefoxdrivername`)
>>
>> 4. Fill in your login credentials in the credentials section

## Add a cron job (*NIX-based OS)
`$ crontab -e`

Paste this:

```bash
1 */1 * * * python3 /path/to/balance.py > /path/to/log-file.log
```

## Windows
Run (and keep it running*)

```bash
python3 C:\path\to\schedule.py
```

# Meta

Thanks to [Telkom KE](http://telkom.co.ke/)

License [MIT](LICENSE)

Have fun...

*I will find a better way ;))

PS: This repo is in no way associated with [Telkom KE](http://telkom.co.ke/) and will definitely be affected by changes in their customer portal.



