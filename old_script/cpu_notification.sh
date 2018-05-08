curl -u username:password -H "Content-Type: application/json" -X POST -d '{
            "recipients":
                        [{"to":"CIOSR8-SGEmployees@bcn.bosch.com"}],
            "subject":{"content":"BuildpackManager Jenkins process down"},
            "body":{
                        "content":"\u003ch1\u003eAlerts!\u003c/h1\u003e\u003cp\u003E BuildpackManager Jenkins process down!\u003cp\u003e",
                        "contentType":"text/html"
            },
            "from": {"eMail":"buildpack-manager-jenkins@bosch-iot.com","password":"xtajBhIG6JZ8HuTlqFHn"}
}'  "http://mail.internal.cn1.bosch-iot-cloud.com/email"

#username/password and smtp url are getting from email services provided.#