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

    private fetch(methodName: String, params: Object) {
        return axios({
            url: baseUrl + this.token + '/' + methodName,
            params: params
        });
    }

    sendMessage(chat_id: Number | String, text: String, parse_mode?: string) {
        this.fetch("sendMessage", { chat_id: chat_id, text: text });
    }
}