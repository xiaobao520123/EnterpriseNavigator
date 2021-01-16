<template>
	<view class="content">
		<image class="logo" src="/static/logo.png"></image>
		<view class="row">
			<view class="text-introduction-area">
				<text class="text-app-name">{{app_name}}</text>
			</view>
		</view>
		<view class="row">
			<view class="text-introduction-area">
				<text class="text-introduction">{{app_introuction}}</text>
			</view>
		</view>
		<view class="row">
			<view class="action-area">
				<button type="primary" @tap="chooseImage"><uni-icons class="uni-icbtn-icon" type="camera" color="white" size="25"></uni-icons>选择一张照片</button>
			</view>
		</view>
		
		<view class="footer">
			<view class="text-footer-area">
				<text class="text-footer-copyright">{{app_copyright}}</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				app_name: '企航',
				app_introuction: '基于深度学习的企业实体识别',
				app_copyright: '© 2020 远航 Studio（中国软件杯）',
				
				server_api_detect: 'http://yourapiserver:5000/api/qcc',
				
				toast_detection_success: '识别成功！',
				toast_upload_file_failed: '上传文件失败，请检查网络设置！',
				toast_server_failed: '服务器错误，错误代码：',
				toast_detection_failed: '识别失败，换一张照片再试试吧～',
				
				image_source_type: ['camera', 'album'],
			}
		},
		onLoad() {

		},
		methods: {
			chooseImage: function() {
				// 呼出uni-app图片选择菜单
				uni.chooseImage({
					count: 1,
					sizeType: ['original', 'compressed'], // 可以指定上传原图还是压缩后的图片（默认：二者均可）
					sourceType: this.image_source_type, // 图片来源（拍照或者相册）
					success: (res) => {
						if (res.tempFilePaths.length == 0) // 如果用户没有选择图片，则直接退出过程
							return;
						let imageSrc = res.tempFilePaths[0]
						
						this.detectEnterpriseFromImage(imageSrc)
						
						uni.showLoading({
							title: '识别中...'
						});
					},
					fail: (err) => {
						// 用户取消选择图片或者应用权限申请失败
					}
				});
			},
			detectEnterpriseFromImage: function(imageFilePath) {
				// 调用uni-app上传文件API，在回调函数中处理识别结果
				uni.uploadFile({
					url: this.server_api_detect,
					filePath: imageFilePath,
					fileType: 'image',
					name: 'data',
					success: (res) => {
						uni.hideLoading()
						let code = res["statusCode"]
						if (code != 200) {
							uni.showToast({
								title: this.toast_server_failed + code,
								duration: 2000,
								icon: 'none'
							})
							return
						}
						let obj = JSON.parse(res["data"])
						let success = obj['success'] // 获取成功标志
						if (success === 0) {
							uni.showToast({
								title: this.toast_detection_failed,
								duration: 2000,
								icon: 'none'
							})
							return
						}
						let enterprise = obj['enterprise']
						uni.showToast({
							title: this.toast_detection_success,
							duration: 2000,
						})
						// 识别成功，跳转到天眼查页面
						uni.navigateTo({
							url: '/pages/index/enterprise-info-view?enterprise=' + encodeURIComponent(JSON.stringify(enterprise))
						})
					},
					fail: (err) => {
						uni.hideLoading()
						uni.showToast({
							title: this.toast_upload_file_failed,
							icon:'none',
							duration: 2000,
						})
					}
				});
			},
		},
	}
</script>

<style>
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.logo {
		height: 200rpx;
		width: 200rpx;
		margin-top: 50rpx;
		margin-left: auto;
		margin-right: auto;
		margin-bottom: 50rpx;
	}
	
	.text-app-name {
		color: #007AFF;
		font-size: xx-large;
		text-align: center;
	}
	
	.text-introduction-area {
		display: flex;
		justify-content: center;
	}
	
	.text-introduction {
		margin-top: 20rpx;
		color: #EE6E73;
		text-align: center;
	}
	
	.footer {
		position: absolute;
		bottom: 0;
		margin-bottom: 100rpx;
	}
	
	.text-footer-area {
		
	}
	
	.text-footer-copyright {
		font-size: medium;
		color: #808080;
	}
	
	.action-area {
		padding: 100rpx;
	}
	
	.uni-icbtn-icon {
		padding-right: 20rpx;
	}
	
</style>
