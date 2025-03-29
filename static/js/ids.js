export function generateRandomString() {
    // Convert the string to an array of characters
    const str = "abcdefghijk";
    let chars = str.split("");

    // Shuffle the array of characters
    for (let i = chars.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [chars[i], chars[j]] = [chars[j], chars[i]];
    }

    // Join the array back into a string
    return chars.join("");
}
