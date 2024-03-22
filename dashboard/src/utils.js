import markdownIt from 'markdown-it';
import markdownItAnchor from 'markdown-it-anchor';
import CryptoJS from 'crypto-js';

const saltLength = 128 / 8;
const hashLength = 128 / 32;

import { customAlphabet } from 'nanoid';
import { ALPHABET } from './constants';

const nanoid = customAlphabet(ALPHABET);

export const md = markdownIt();
const defaultRender =
  md.renderer.rules.link_open ||
  function (tokens, idx, options, env, self) {
    return self.renderToken(tokens, idx, options);
  };
md.use(markdownItAnchor, {});
md.renderer.rules.link_open = function (tokens, idx, options, env, self) {
  tokens[idx].attrSet('target', '_blank');
  return defaultRender(tokens, idx, options, env, self);
};

export function shortDate() {
  return new Date().toISOString().split('T')[0].replace(/-/g, '').substring(2);
}

export function randomId(len) {
  return nanoid(len);
}

export function joinPath(...parts) {
  const separator = '/';
  const replace = new RegExp(separator + '{1,}', 'g');
  return parts.join(separator).replace(replace, separator);
}

export function delay(duration) {
  return new Promise((resolve) => setTimeout(resolve, duration));
}

export function getFileName(path) {
  return path.split('/').slice(-1)[0];
}

export function hash(
  password,
  salt = CryptoJS.lib.WordArray.random(saltLength).toString()
) {
  return (
    salt +
    CryptoJS.PBKDF2(password, salt, {
      keySize: hashLength,
      iterations: 64
    }).toString()
  );
}

export function verify(password, raw) {
  const salt = raw.substring(0, saltLength * 2);
  const compareWithHash = hash(password, salt);
  return raw === compareWithHash;
}

export function encrypt(text, pass) {
  return CryptoJS.AES.encrypt(text, pass).toString();
}

export function decrypt(cipher, pass) {
  return CryptoJS.AES.decrypt(cipher, pass).toString(CryptoJS.enc.Utf8);
}
