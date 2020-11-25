import { Http2ServerRequest } from "http2";

import https from 'https';
import url from 'url';
import axios from 'axios';

const baseUrl = 'https://api.telegram.org/bot';

export default class TelegramApi {
    private token: String;

    constructor(token: String) {
        this.token = token;
    }

    private async fetch(methodName: String, params: Object) {
        return axios({
            url: baseUrl + this.token + '/' + methodName,
            params: params,
            method: 'POST'
        });
    }

    async sendMessage(chat_id: Number | String, text: String, parse_mode?: string) {
        return this.fetch("sendMessage", { chat_id: chat_id, text: text });
    }

    async setWebhook(url: String) {
        return this.fetch("setWebhook", { url: url });
    }

    async getWebhookInfo() {
        return this.fetch("getWebhookInfo",{});
    }
}