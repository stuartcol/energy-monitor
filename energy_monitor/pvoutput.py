import urllib
import httplib
import logging
import socket
from httplib import BadStatusLine


class Connection():
    def __init__(self, api_key, system_id, host='pvoutput.org'):
        self.host = host
        self.api_key = api_key
        self.system_id = system_id

        self.logger = logging.getLogger(__name__)

    def add_output(self, date, generated=None, exported=None, peak_power=None,
                   peak_time=None, condition=None,
                   min_temp=None, max_temp=None, comments=None,
                   import_peak=None,
                   import_offpeak=None, import_shoulder=None):
        """
        Uploads end of day output information
        """
        path = '/service/r1/addoutput.jsp'
        params = {
            'd': date,
        }
        if generated:
            params['g'] = generated
        if exported:
            params['e'] = exported
        if peak_power:
            params['pp'] = peak_power
        if peak_time:
            params['pt'] = peak_time
        if condition:
            params['cd'] = condition
        if min_temp:
            params['tm'] = min_temp
        if max_temp:
            params['tx'] = max_temp
        if comments:
            params['cm'] = comments
        if import_peak:
            params['ip'] = import_peak
        if import_offpeak:
            params['op'] = import_offpeak
        if import_shoulder:
            params['is'] = import_shoulder

        for k, v in params.iteritems():
            self.logger.info("Using key: {0} with value: {1}".format(k, v))

        params = urllib.urlencode(params)

        response = self.make_request('POST', path, params)

        if response.status == 400:
            self.logger.error(response.read())
        if response.status != 200:
            self.logger.error(response.read())

    def add_status(self, date, time, energy_exp=None, power_exp=None,
                   energy_imp=None, power_imp=None, temp=None, vdc=None,
                   cumulative=False, net=False, v7=None, v8=None, v9=None,
                   v10=None, v11=None, v12=None):
        """
        Uploads live output data

        """

        path = '/service/r2/addstatus.jsp'
        params = {
            'd': date,
            't': time
        }

        if energy_exp:
            params['v1'] = energy_exp
        if power_exp >= 0.0:
            params['v2'] = power_exp
        if energy_imp:
            params['v3'] = energy_imp
        if power_imp:
            params['v4'] = power_imp
        if temp:
            params['v5'] = temp
        if vdc:
            params['v6'] = vdc
        if v7:
            params['v7'] = v7
        if v8:
            params['v8'] = v8
        if v9:
            params['v9'] = v9
        if v10:
            params['v10'] = v10
        if v11:
            params['v11'] = v11
        if v12:
            params['v12'] = v12
        if cumulative:
            params['c1'] = 1
        if net:
            params['n'] = 1

        for k, v in params.iteritems():
            self.logger.info("Using key: {0} with value: {1}".format(k, v))

        params = urllib.urlencode(params)

        self.logger.debug(params)

        response = self.make_request('POST', path, params)

        self.logger.debug(response)

        # if response.status == 400:
        #     self.logger.error(response.read())
        # if response.status != 200:
        #     self.logger.error(response.read())

    def get_status(self, date=None, time=None):
        """
        Retrieves status information
        """
        path = '/service/r1/getstatus.jsp'
        params = {}
        if date:
            params['d'] = date
        if time:
            params['t'] = time
        params = urllib.urlencode(params)

        response = self.make_request("GET", path, params)

        if response.status == 400:
            raise ValueError(response.read())
        if response.status != 200:
            raise StandardError(response.read())

        return response.read()

    def delete_status(self, date, time):
        """
        Removes an existing status
        """
        path = '/service/r1/deletestatus.jsp'
        params = {
            'd': date,
            't': time
        }
        params = urllib.urlencode(params)

        response = self.make_request("POST", path, params)

        if response.status == 400:
            raise ValueError(response.read())
        if response.status != 200:
            raise StandardError(response.read())

        return response.read()

    def make_request(self, method, path, params=None):
        conn = httplib.HTTPConnection(self.host)
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain',
            'X-Pvoutput-Apikey': self.api_key,
            'X-Pvoutput-SystemId': self.system_id
        }

        try:
            conn.request(method, path, params, headers)
        except Exception as e:
        #except:

            self.logger.error(e)
            return

        return conn.getresponse()
