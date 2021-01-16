<template>
	<view>
		<web-view :src="url" @message="getMessage"></web-view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				url: 'https://m.tianyancha.com/search?key=' // 天眼查搜索引擎网址
			}
		},
		onLoad(options) {
			if (options && options.enterprise) {
				const enterprise = JSON.parse(decodeURIComponent(options.enterprise));
				this.url = this.url + enterprise
			}
		},
		methods: {
			getMessage(event) {
				uni.showModal({
					content: JSON.stringify(event.detail),
					showCancel: false
				});
			}
		}
	}
</script>

<style>

</style>
