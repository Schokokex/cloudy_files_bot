import FormData from "form-data";
import { request } from 'https';
import { createReadStream } from "fs";
import axios from 'axios';

const baseUrl = 'https://api.telegram.org/bot';

export default class TelegramApi {
    private token: String;

    constructor(token: String) {
        this.token = token;
    }

    private async fetch(methodName: String, params: Object) {
        const form = new FormData();
        for (const key in params) {
            form.append(key, params[key]);
        }
        // return new Promise((resolve, rej) => {
        //     form.pipe(request({
        //         host: baseUrl + this.token,
        //         path: '/' + methodName,
        //         method: 'POST',
        //         headers: form.getHeaders(),
        //     }, resolve));
        // })
        return axios({
            method: 'post',
            url: baseUrl + this.token + '/' + methodName,
            headers: {
                ...form.getHeaders()
            },
            data: form
        })
    }

    async sendMessage(chat_id: Number | String, text: String, parse_mode?: string) {
        return this.fetch("sendMessage", { chat_id: chat_id, text: text });
    }

    async setWebhook(url: String, certificatePath?: string) {
        return certificatePath
            && this.fetch("setWebhook", { url: url, certificate: createReadStream(certificatePath) })
            || this.fetch("setWebhook", { url: url });
    }

    async getWebhookInfo() {
        return this.fetch("getWebhookInfo", {});
    }
}